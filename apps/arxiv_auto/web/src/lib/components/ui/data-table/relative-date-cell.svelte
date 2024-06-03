<script lang="ts">
	import { Label } from '$lib/components/ui/label';
	import { formatDistanceToNowStrict } from 'date-fns';

	export let date: string | null = '';
</script>

<Label>
	{#if date}
		{formatDistanceToNowStrict(date, { addSuffix: true })}
	{:else}
		Never
	{/if}
</Label>
