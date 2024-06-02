<script lang="ts">
	import * as Resizable from '$lib/components/ui/resizable';
	import DataTable from '$lib/components/ui/data-table/data-table.svelte';
	import { LeadViewer } from '$lib/components/ui/lead-viewer';
	import type { Lead } from '$lib/types';

	export let data: { leads: Lead[] };
	let { leads } = data;

	let activeLead: Lead = leads[0];
</script>

<Resizable.PaneGroup direction="horizontal" class="rounded-lg border">
	<Resizable.Pane defaultSize={50}>
		<div class="flex items-center justify-center p-6">
			<DataTable bind:activeLead data={leads} />
		</div>
	</Resizable.Pane>
	<Resizable.Handle withHandle />
	<Resizable.Pane defaultSize={50}>
		<LeadViewer bind:lead={activeLead} />
	</Resizable.Pane>
</Resizable.PaneGroup>
