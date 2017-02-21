# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.forms import HiddenInput, MultipleHiddenInput, Widget
from django.forms.utils import flatatt
from django.utils.encoding import force_text
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _


class FilterWidgetMixin(object):
    class Media:
        js = ("js/foreign_key_widget.js",)

    @staticmethod
    def render_input_filter():
        return format_html('<input type="text" class="input-filter" '
                           'style="width:286px;display:block" placeholder="{}" />'
                           .format(_("Search")))

    @staticmethod
    def render_input_filter_results():
        return format_html(
            '<select multiple class="filter-result" style="width:300px;display:block"></select>')

    def render_selected_options(self, values):
        if values is None or values == "":
            return ""
        if not isinstance(values, list):
            values = [values]
        items_selected = []
        choices = self.choices.queryset.filter(pk__in=values)
        for choice in choices:
            option_value, option_label = self.choices.choice(choice)
            items_selected.append('<li value="{}">{}</li>'.format(option_value, force_text(option_label)))
        return '\n'.join(items_selected)

    def render_selected_widget(self, values):
        items_selected = self.render_selected_options(values)
        return format_html('<ul style="display:block">{}</ul>'.format(items_selected))

    def render_filter_widget(self, values, widget, name, attrs=None):
        final_attrs = self.build_attrs(attrs, name=name, multiple=self.is_multiple)
        selected_items = self.render_selected_widget(values)
        input_filter = self.render_input_filter()
        input_filter_results = self.render_input_filter_results()
        return format_html('<div class="filter-widget" {}>'
                           '<div class="form-send">{}</div> '
                           '{selected_items} {input_filter} '
                           '<div class="loading" style="visibility:hidden">{loading}...</div> '
                           '{input_filter_results}'
                           '</div>'
                           .format(flatatt(final_attrs),
                                   widget,
                                   selected_items=selected_items,
                                   input_filter=input_filter,
                                   loading=_('Loading'),
                                   input_filter_results=input_filter_results))


class ForeignKeyWidget(HiddenInput, FilterWidgetMixin):
    is_multiple = 0

    @property
    def is_hidden(self):
        return False

    def render(self, name, value, attrs=None):
        hidden_input = super(ForeignKeyWidget, self).render(name, value, attrs)
        return self.render_filter_widget(values=value, widget=hidden_input, name=name, attrs=attrs)


class ManyToManyWidget(MultipleHiddenInput, FilterWidgetMixin):
    is_multiple = 1

    @property
    def is_hidden(self):
        return False

    def render(self, name, value, attrs=None):
        hidden_inputs = super(ManyToManyWidget, self).render(name, value, attrs)
        return self.render_filter_widget(values=value, widget=hidden_inputs, name=name, attrs=attrs)
