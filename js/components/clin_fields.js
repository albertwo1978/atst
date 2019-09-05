import DateSelector from './date_selector'
import { emitEvent } from '../lib/emitters'
import Modal from '../mixins/modal'
import optionsinput from './options_input'
import textinput from './text_input'

const START_DATE = 'start_date'
const END_DATE = 'end_date'
const POP = 'period_of_performance'
const NUMBER = 'number'

export default {
  name: 'clin-fields',

  components: {
    DateSelector,
    optionsinput,
    textinput,
  },

  mixins: [Modal],

  props: {
    initialClinIndex: Number,
    initialStartDate: {
      type: String,
      default: null,
    },
    initialEndDate: {
      type: String,
      default: null,
    },
    initialClinNumber: {
      type: String,
      default: null,
    },
  },

  data: function() {
    const start = !!this.initialStartDate
      ? new Date(this.initialStartDate)
      : undefined
    const end = !!this.initialEndDate
      ? new Date(this.initialEndDate)
      : undefined
    const popValidation = !this.initialStartDate ? false : start < end
    const showPopValidation = !this.initialStartDate ? false : !popValidation
    const clinNumber = !!this.initialClinNumber
      ? this.initialClinNumber
      : undefined

    return {
      clinIndex: this.initialClinIndex,
      startDate: start,
      endDate: end,
      popValid: popValidation,
      showPopError: showPopValidation,
      clinNumber: clinNumber,
      showClin: true,
    }
  },

  mounted: function() {
    this.$root.$on('field-change', this.handleFieldChange)
  },

  created: function() {
    emitEvent('field-mount', this, {
      optional: false,
      name: 'clins-' + this.clinIndex + '-' + POP,
      valid: this.checkPopValid(),
    })
  },

  methods: {
    checkPopValid: function() {
      return this.startDate < this.endDate
    },

    validatePop: function() {
      if (!!this.startDate && !!this.endDate) {
        // only want to update popValid and showPopError if both dates are filled in
        this.popValid = this.checkPopValid()
        this.showPopError = !this.popValid
      }

      emitEvent('field-change', this, {
        name: 'clins-' + this.clinIndex + '-' + POP,
        valid: this.checkPopValid(),
      })
    },

    handleFieldChange: function(event) {
      if (this._uid === event.parent_uid) {
        if (event.name.includes(START_DATE)) {
          if (!!event.value) this.startDate = new Date(event.value)
          this.validatePop()
        } else if (event.name.includes(END_DATE)) {
          if (!!event.value) this.endDate = new Date(event.value)
          this.validatePop()
        } else if (event.name.includes(NUMBER)) {
          this.clinNumber = event.value
        }
      }
    },

    removeClin: function() {
      this.showClin = false
      emitEvent('remove-clin', this, {
        clinIndex: this.clinIndex,
      })
      this.closeModal('remove_clin')
    },
  },

  computed: {
    clinTitle: function() {
      if (!!this.clinNumber) {
        return `CLIN ${this.clinNumber}`
      } else {
        return `CLIN`
      }
    },

    removeModalId: function() {
      return `remove-clin-${this.clinIndex}`
    },
  },
}
