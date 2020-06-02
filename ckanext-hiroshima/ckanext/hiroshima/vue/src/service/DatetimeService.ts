import Moment from 'moment/moment'

export default {
  JST: 9,
  HOURS: 24,
  namespaced: true,

  getDateAtUTC: (diff: number) => {
    return Moment(new Date()).add('days', diff).utc().format()
  },

  getHour: (time: string) => {
    return Moment(time).format('H時')
  },
}
