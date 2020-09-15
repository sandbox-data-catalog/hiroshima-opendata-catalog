/**
 * 指定ミリ秒だけ処理を遅らせる
 * @param {Number} waitTime
 */
export const sleep = async (waitTime: number) => {
  await new Promise((resolve) => setTimeout(() => resolve(), waitTime))
}
