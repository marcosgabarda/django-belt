import {forEach, find} from 'lodash';

(function () {
  "use strict";
  const TIME_WAITING_BEFORE_SEARCH = 1000,
    MINIMUM_SEARCH_LENGTH = 3;

  window.addEventListener('load', initForeignKeyWidget, false);

  function initForeignKeyWidget() {
    let inputs = document.getElementsByClassName('filter-widget');
    forEach(inputs, (element) => new ForeignKeyWidget(element));
  }

  class ForeignKeyWidget {
    constructor(container) {
      this.timeoutID = 0;
      this.isMultiple = container.getAttribute('multiple') == 1;
      this.name = container.getAttribute('name');
      this.url = container.getAttribute('url');
      this.searchField = container.getAttribute('search-field');
      this.label = container.getAttribute('label-name') || this.searchField;
      this.loading = find(container.children, (element) => element.className === "loading");
      this.inputFilter = find(container.children, (element) => element.className === "input-filter");
      this.inputResult = find(container.children, (element) => element.className === "filter-result");
      this.selected = find(container.children, (element) => element.tagName === "UL");
      this.inputFilter.onkeyup = () => this.handleOnKeyPress(this.inputFilter.value);
      this.inputResult.onchange = this.handleChange.bind(this);
      this.formSend = find(container.children, (element) => element.className === "form-send");
      if (this.isMultiple) {
        this.addValue = this.addMultiple;
        this.selected.onclick = (event) => this.deleteMultiple(event.target);
      } else {
        this.addValue = this.addOne;
        this.selected.onclick = (event) => this.deleteOne(event.target);
      }
    }

    handleOnKeyPress(value) {
      this.clearChildren(this.inputResult);
      window.clearTimeout(this.timeoutID);
      if (value.length < MINIMUM_SEARCH_LENGTH) {
        return;
      }
      this.loading.style.visibility = "visible";
      this.timeoutID = window.setTimeout(() => {
        this.search(value);
      }, TIME_WAITING_BEFORE_SEARCH);
    }

    search(value) {
      const url = `${this.url}?${this.searchField}=${value}`;
      fetch(url, {
        credentials: 'same-origin',
        method: 'get',
      }).then((response) => response.json())
        .then(({objects}) => {
          this.addOptions(objects);
          this.loading.style.visibility = "hidden";
        })
    }

    addOptions(items) {
      forEach(items, (item) => {
        let option = document.createElement("option");
        option.text = item[this.label];
        option.value = item.id;
        this.inputResult.appendChild(option);
      })
    }

    clearChildren(element) {
      while (element.firstChild) {
        element.removeChild(element.firstChild);
      }
    }

    handleChange(event) {
      const value = event.target.options[event.target.options.selectedIndex].value;
      const text = event.target.options[event.target.options.selectedIndex].text;
      this.addValue(value);
      let li = document.createElement("li");
      li.value = value;
      li.textContent = text;
      this.selected.appendChild(li);
    }

    addOne(value) {
      this.clearChildren(this.selected);
      find(this.formSend.children, (element) => element.type === "hidden").value = value;
    }

    addMultiple(value) {
      let input = document.createElement("input");
      input.type = "hidden";
      input.name = this.name;
      input.value = value;
      this.formSend.appendChild(input);
    }

    deleteOne(target) {
      find(this.formSend.children, (element) => element.type === "hidden").value = "";
      target.remove();
    }

    deleteMultiple(target) {
      find(this.formSend.children, (element) => element.value == target.value).remove();
      target.remove();
    }
  }
})();
