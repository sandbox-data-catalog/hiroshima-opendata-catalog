export default {
  namespaced: true,

  /**
   * 日付型から文字列にフォーマットする
   * @param  {Date}   date
   * @return {String} ****年 *月**日
   */
  dateToStringJp: (date: Date): string => {
    return `${date.getFullYear()}年${('  ' + (date.getMonth() + 1)).substr(
      -2
    )}月${('  ' + date.getDate()).substr(-2)}日`
  },
}
