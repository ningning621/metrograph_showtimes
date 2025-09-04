<script>
	/** @type {String} class="flex justify-center" - classes to apply to the wrapper */

	/**
	 * @typedef {Object} Props
	 * @property {String} [label]
	 * @property {Boolean} hideLabel={true} [hideLabel]
	 * @property {Number} [min]
	 * @property {Number} [max]
	 * @property {Number} [step]
	 * @property {Number} value
	 * @property {any} class
	 * @property {String} style
	 */

	/** @type {Props} */
	let {
		label = '',
		hideLabel = false,
		min = 1,
		max = 100,
		step = 1,
		value = $bindable(),
		class: classes,
		style
	} = $props();
</script>

<label class={classes} {style}>
	<span class:hidden={hideLabel}>{label}</span>
	<input
		class:cursor-ew-resize={value !== min && value !== max}
		class:cursor-e-resize={value === min}
		class:cursor-w-resize={value === max}
		type="range"
		{min}
		{max}
		{step}
		bind:value
	/>
</label>

<style lang="postcss">
	@reference '$lib/styles/app.css';

	input {
		@apply appearance-none;
		background: var(--trackBackground, #cecece);
		border: var(--trackBorder, none);
		border-radius: var(--trackBorderRadius, 0);
		height: var(--trackHeight, 4px);
		width: var(--trackWidth, 150px);
	}

	/* thumb styles */
	input::-webkit-slider-thumb {
		@apply appearance-none;
		background: var(--thumbBackground, #000);
		border: var(--thumbBorder, none);
		border-radius: var(--thumbBorderRadius, 50%);
		box-shadow: var(--thumbBoxShadow, none);
		height: var(--thumbHeight, var(--thumbWidth, 12px));
		width: var(--thumbWidth, var(--thumbHeight, 12px));
	}

	input::-moz-range-thumb {
		@apply appearance-none;
		background: var(--thumbBackground, #000);
		border: var(--thumbBorder, none);
		border-radius: var(--thumbBorderRadius, 50%);
		box-shadow: var(--thumbBoxShadow, none);
		height: var(--thumbHeight, var(--thumbWidth, 12px));
		width: var(--thumbWidth, var(--thumbHeight, 12px));
	}

	input::-ms-thumb {
		@apply appearance-none;
		background: var(--thumbBackground, #000);
		border: var(--thumbBorder, none);
		border-radius: var(--thumbBorderRadius, 50%);
		box-shadow: var(--thumbBoxShadow, none);
		height: var(--thumbHeight, var(--thumbWidth, 12px));
		width: var(--thumbWidth, var(--thumbHeight, 12px));
	}

	/* reset tracks, use input itself */
	input::-webkit-slider-runnable-track {
		@apply appearance-none border-none bg-transparent shadow-none;
	}
	input::-moz-range-track {
		@apply appearance-none border-none bg-transparent shadow-none;
	}
	input::-ms-track {
		@apply appearance-none border-none bg-transparent shadow-none;
	}
</style>
