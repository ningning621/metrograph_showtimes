/**
 * @description Check if a number is between two other numbers
 * @param {Number} value - The number to check
 * @param {[Number, Number]} range - The range to check against
 * @returns {Boolean} - True if the value is within the range, false otherwise
 */
export default (value: string | number, [min, max]: [number, number]) =>
	+value >= +min && +value <= +max;
