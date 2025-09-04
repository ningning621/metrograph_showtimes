/**
 * @function
 * @name outclick
 * @description Dispatch event on click outside of node
 * @param {Element} node - the node to which the outclick should be applied
 * @param {Function} cb - the callback to be executed on outclick
 * @see {@link https://svelte.dev/tutorial/actions|Svelte docs}
 * @example <div use:outclick on:outclick={() => alert('Beep Boop')}>Hello World.</div>
 */
export default (node: HTMLElement, cb?: () => void) => {
	const handleClick = (event: MouseEvent) => {
		if (node && !node.contains(event.target as Node) && !event.defaultPrevented) {
			node.dispatchEvent(new CustomEvent('outclick', { detail: node }));
			if (cb) cb();
		}
	};

	document.addEventListener('click', handleClick, true);

	return {
		destroy() {
			document.removeEventListener('click', handleClick, true);
		}
	};
};
