import 'svg-innerhtml'
import 'babel-polyfill'
import ally from 'ally.js'

import classes from '../styles/atat.scss'
import Vue from 'vue/dist/vue'
import VTooltip from 'v-tooltip'
import stickybits from 'stickybits'

import dodlogin from './components/dodlogin'
import optionsinput from './components/options_input'
import multicheckboxinput from './components/multi_checkbox_input'
import textinput from './components/text_input'
import checkboxinput from './components/checkbox_input'
import poc from './components/forms/poc'
import toggler from './components/toggler'
import ApplicationNameAndDescription from './components/forms/new_application/name_and_description'
import ApplicationEnvironments from './components/forms/new_application/environments'
import MultiStepModalForm from './components/forms/multi_step_modal_form'
import uploadinput from './components/upload_input'
import Modal from './mixins/modal'
import selector from './components/selector'
import BudgetChart from './components/charts/budget_chart'
import SpendTable from './components/tables/spend_table'
import EnvironmentsTable from './components/tables/application_environments'
import LocalDatetime from './components/local_datetime'
import { isNotInVerticalViewport } from './lib/viewport'
import DateSelector from './components/date_selector'
import SidenavToggler from './components/sidenav_toggler'
import BaseForm from './components/forms/base_form'
import DeleteConfirmation from './components/delete_confirmation'
import NewEnvironment from './components/forms/new_environment'
import EnvironmentRole from './components/environment_role'
import SemiCollapsibleText from './components/semi_collapsible_text'
import ToForm from './components/forms/to_form'
import ClinFields from './components/clin_fields'

Vue.config.productionTip = false

Vue.use(VTooltip)

Vue.mixin(Modal)

const app = new Vue({
  el: '#app-root',
  components: {
    dodlogin,
    toggler,
    optionsinput,
    multicheckboxinput,
    textinput,
    checkboxinput,
    poc,
    ApplicationNameAndDescription,
    ApplicationEnvironments,
    selector,
    BudgetChart,
    SpendTable,
    EnvironmentsTable,
    LocalDatetime,
    MultiStepModalForm,
    uploadinput,
    DateSelector,
    SidenavToggler,
    BaseForm,
    DeleteConfirmation,
    NewEnvironment,
    EnvironmentRole,
    SemiCollapsibleText,
    ToForm,
    ClinFields,
  },

  mounted: function() {
    this.$on('modalOpen', data => {
      if (data['isOpen']) {
        document.body.className += ' modal-open'
        this.activeModal = data['name']

        var handler = ally.maintain.disabled({
          filter: `#${this.modalId}`,
        })

        this.allyHandler = handler
      } else {
        this.activeModal = null
        if (this.allyHandler) {
          this.allyHandler.disengage()
          this.allyHandler = null
        }
        document.body.className = document.body.className.replace(
          ' modal-open',
          ''
        )
      }
    })

    const modalOpen = document.querySelector('#modalOpen')

    if (modalOpen) {
      const modal = modalOpen.getAttribute('data-modal')
      this.openModal(modal)
    }

    ally.query.focusable().forEach(function(el) {
      el.addEventListener('focus', function() {
        if (isNotInVerticalViewport(el)) {
          el.scrollIntoView({ block: 'center' })
        }
      })
    })
  },
  delimiters: ['!{', '}'],

  directives: {
    sticky: {
      inserted: (el, binding) => {
        var customAttributes
        if (binding.expression) {
          customAttributes = JSON.parse(binding.expression)
        }
        stickybits(el, customAttributes)
      },
    },
  },
})
