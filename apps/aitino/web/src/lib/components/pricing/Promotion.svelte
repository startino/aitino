<script lang="ts">
	export let activeTabValue = 0;
</script>

<label
	for={$$props.for}
	class="{$$props.class} title-medium flex flex-row gap-2 rounded tracking-wide"
>
	{$$props.text}
	<slot />
</label>
<input
	type="radio"
	name={$$props.name}
	class="hidden peer/{$$props.for}"
	bind:group={activeTabValue}
	value={$$props.value}
	id={$$props.for}
/>
