<!-- 
  @component A basic scrollytelly template that accepts two slots for a background and foreground, built off a scrollytelly helper from Rich Harris & Svelte (https://github.com/sveltejs/svelte-scroller)
	@slot background - The fixed background node - typically a graphic
	@slot foreground - copy or other content that scrolls as steps
 -->
<script>
	import Scroller from '@sveltejs/svelte-scroller';
	let index = $state();
	let progress = $state();
</script>

<Scroller top={0} bottom={1} threshold={0.5} bind:index bind:progress>
	{#snippet background()}
		<div
			id=""
			class="flex h-screen w-100 flex-col items-center justify-center px-4 transition-colors duration-1000 ease-linear"
			class:bg-secondary={!index}
			class:bg-tertiary={index === 1}
			class:bg-offset={index === 2}
		>
			<h2 class="text-4xl font-bold uppercase">
				Step {index}
			</h2>
			<div class="bg-secondary mt-4 block w-full border">
				<span class="block h-4 w-full max-w-full" style:width="{(progress || 0) * 100}%"></span>
			</div>
		</div>
	{/snippet}

	{#snippet foreground()}
		{#each Array.from({ length: 3 }) as _, i}
			<section
				class="step mx-auto flex h-[80vh] flex-row flex-wrap items-center transition duration-300 ease-in last-of-type:h-screen"
				class:opacity-40={i !== index}
			>
				<div class="bg-primary w-100 w-full rounded-sm border px-4 py-3 shadow-lg">
					<p class="my-2 w-full text-left text-base">
						Lorem ipsum, dolor sit amet consectetur adipisicing elit. Minus ea provident delectus
						molestias accusantium. Quibusdam quos neque veritatis, magnam sit blanditiis vitae id
						iusto, dolor, sunt cumque incidunt. Neque, eum?
					</p>
				</div>
			</section>
		{/each}
	{/snippet}
</Scroller>
