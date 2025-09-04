export function focusableChildren(node: HTMLElement) {
	const nodes = Array.from(
		node.querySelectorAll(
			'a[href], button, input, textarea, select, details, [tabindex]:not([tabindex="-1"])'
		)
	);

	const activeElement = document.activeElement as HTMLElement | null;
	const index = activeElement ? nodes.indexOf(activeElement) : -1;

	const update = (d: number) => {
		let i = index + d;
		i += nodes.length;
		i %= nodes.length;

		(nodes[i] as HTMLElement)?.focus();
	};

	return {
		next: (selector?: string) => {
			const reordered = [...nodes.slice(index + 1), ...nodes.slice(0, index + 1)];

			for (let i = 0; i < reordered.length; i += 1) {
				if (!selector || reordered[i].matches(selector)) {
					(reordered[i] as HTMLElement).focus();
					return;
				}
			}
		},

		prev: (selector?: string) => {
			const reordered = [...nodes.slice(index + 1), ...nodes.slice(0, index + 1)];

			for (let i = reordered.length - 2; i >= 0; i -= 1) {
				if (!selector || reordered[i].matches(selector)) {
					(reordered[i] as HTMLElement).focus();
					return;
				}
			}
		},
		update
	};
}

export function trap(node: HTMLElement, { resetFocus = true }: { resetFocus?: boolean } = {}) {
	if (!node || !document.activeElement) return;

	const previous: Element = document.activeElement;

	const handleKeydown = (e: KeyboardEvent) => {
		if (e.key === 'Tab') {
			e.preventDefault();

			const group = focusableChildren(node);
			if (e.shiftKey) {
				group.prev();
			} else {
				group.next();
			}
		}
	};

	node.addEventListener('keydown', handleKeydown);

	return {
		destroy: () => {
			node.removeEventListener('keydown', handleKeydown);
			if (resetFocus) {
				(previous as HTMLElement)?.focus({ preventScroll: true });
			}
		}
	};
}
