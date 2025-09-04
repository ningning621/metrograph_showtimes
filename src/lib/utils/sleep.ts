/**
 * Sleep for a given amount of time.
 *
 * @param ms - The amount of time to sleep in milliseconds.
 * @returns A promise that resolves after the given amount of time.
 * @example
 * ```js
 * await sleep(1000);
 * ```
 */
export default (ms: number): Promise<void> => new Promise((resolve) => setTimeout(resolve, ms));
