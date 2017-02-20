# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division, absolute_import

from django.contrib.admin.utils import quote
from django.forms.widgets import Widget
from django.template.defaultfilters import truncatechars
from django.urls import reverse
from django.utils.encoding import smart_text
from django.utils.safestring import mark_safe


class ManyToManyListAdmin(Widget):
    class Media:
        js = ("js/foreign_key_widget.js",)

    @staticmethod
    def _format_item(item):
        url = reverse('admin:%s_%s_change' % (item._meta.app_label, item._meta.model_name),
                      args=(quote(item.pk),), )
        label = truncatechars(smart_text(item), 40)
        return "<a href='{}'>{}</a>".format(url, label)

    def render(self, name, value, attrs=None):
        selected_values = self.choices.queryset.filter(id__in=value)
        return mark_safe(
            "".join(
                ["<ul>"] + map(lambda item: "<li>%s</li>" % self._format_item(item), selected_values) + ["</ul>"]
            )
        )
