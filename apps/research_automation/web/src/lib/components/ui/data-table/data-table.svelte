<script lang="ts">
	import { Render, createRender } from '$lib/svelte-render';
	import { createTable, Subscribe } from '$lib/svelte-headless-table';
	import {
		addSortBy,
		addPagination,
		addTableFilter,
		addSelectedRows,
		addHiddenColumns
	} from '$lib/svelte-headless-table/plugins';
	import { readable } from 'svelte/store';
	import * as Table from '$lib/components/ui/table';
	import * as Sheet from '$lib/components/ui/sheet';
	import { Label } from '$lib/components/ui/label';
	import Actions from '$lib/components/ui/data-table/data-table-actions.svelte';
	import { Button } from '$lib/components/ui/button';
	// TODO: Replace radix with lucide icons, radix hasn't had an update in 2 years
	import { CaretSort, ChevronDown } from 'radix-icons-svelte';
	import { ArrowUpDown } from 'lucide-svelte';
	import * as DropdownMenu from '$lib/components/ui/dropdown-menu';
	import { cn } from '$lib/utils';
	import { Input } from '$lib/components/ui/input';
	import DataTableCheckbox from '$lib/components/ui/data-table/data-table-checkbox.svelte';
	import type { building } from '$app/environment';
	import type { Lead } from '$lib/types';
	import StatusCell from './status-cell.svelte';
	import RelativeDateCell from './relative-date-cell.svelte';

	export let activeLead: Lead | null = null;
	export let data: Lead[] = [];

	const table = createTable(readable(data), {
		sort: addSortBy({ disableMultiSort: true }),
		page: addPagination(),
		filter: addTableFilter({
			fn: ({ filterValue, value }) => value.includes(filterValue)
		}),
		select: addSelectedRows(),
		hide: addHiddenColumns()
	});

	const columns = table.createColumns([
		table.column({
			header: 'Prospect Username',
			accessor: 'prospect_username'
		}),
		table.column({
			header: 'Status',
			accessor: 'status',
			cell: (item) => {
				return createRender(StatusCell, {
					status: item.value
				});
			}
		}),
		table.column({
			header: 'Discovered At',
			accessor: 'discovered_at',
			cell: (item) => {
				return createRender(RelativeDateCell, {
					date: item.value ?? ''
				});
			}
		}),
		table.column({
			header: '',
			accessor: ({ id }) => id,
			cell: (item) => {
				return createRender(Actions, { id: item.value });
			},
			plugins: {
				sort: {
					disable: true
				}
			}
		})
	]);

	const { headerRows, pageRows, tableAttrs, tableBodyAttrs, flatColumns, pluginStates, rows } =
		table.createViewModel(columns);

	const { sortKeys } = pluginStates.sort;

	const { hiddenColumnIds } = pluginStates.hide;
	const ids = flatColumns.map((c) => c.id);
	let hideForId = Object.fromEntries(ids.map((id) => [id, true]));

	$: $hiddenColumnIds = Object.entries(hideForId)
		.filter(([, hide]) => !hide)
		.map(([id]) => id);

	const { hasNextPage, hasPreviousPage, pageIndex } = pluginStates.page;
	const { filterValue } = pluginStates.filter;

	const { selectedDataIds } = pluginStates.select;

	const hideableCols = ['status', 'amount'];
</script>

<div class="w-full">
	<div class="mb-4 flex items-center gap-4">
		<Input
			class="max-w-sm"
			placeholder="Filter using id or smt..."
			type="text"
			bind:value={$filterValue}
		/>
	</div>
	<div class="rounded-md border">
		<Table.Root {...$tableAttrs}>
			<Table.Header>
				{#each $headerRows as headerRow}
					<Subscribe rowAttrs={headerRow.attrs()}>
						<Table.Row>
							{#each headerRow.cells as cell (cell.id)}
								<Subscribe attrs={cell.attrs()} let:attrs props={cell.props()} let:props>
									<Table.Head {...attrs} class={cn('[&:has([role=checkbox])]:pl-3')}>
										{#if cell.id === 'last_event' || cell.id === 'status' || cell.id === 'discovered_at'}
											<Button variant="ghost" on:click={props.sort.toggle}>
												<Render of={cell.render()} />
												<ArrowUpDown class={'ml-2 h-4 w-4'} />
											</Button>
										{:else}
											<Render of={cell.render()} />
										{/if}
									</Table.Head>
								</Subscribe>
							{/each}
						</Table.Row>
					</Subscribe>
				{/each}
			</Table.Header>
			<Table.Body {...$tableBodyAttrs}>
				{#each $pageRows as row (row.id)}
					<Subscribe rowAttrs={row.attrs()} let:rowAttrs>
						<Table.Row
							{...rowAttrs}
							data-state={$selectedDataIds[row.id] && 'selected'}
							on:click={() => {
								activeLead = data.find((d) => d.id === row.original.id) ?? null;
							}}
						>
							{#each row.cells as cell (cell.id)}
								<Subscribe attrs={cell.attrs()} let:attrs>
									<Table.Cell class="text-start [&:has([role=checkbox])]:pl-3" {...attrs}>
										{#if cell.id === 'status'}
											<div
												class="font-medium uppercase {cell.render() == 'under_review'
													? 'text-yellow-600'
													: 'text-foreground'}"
											>
												<Render of={cell.render()} />
											</div>
										{:else}
											<Render of={cell.render()} />
										{/if}
									</Table.Cell>
								</Subscribe>
							{/each}
						</Table.Row>
					</Subscribe>
				{/each}
			</Table.Body>
		</Table.Root>
	</div>
	<div class="flex items-center justify-end space-x-2 py-4">
		<div class="flex-1 text-sm text-muted-foreground">
			{Object.keys($selectedDataIds).length} of{' '}
			{$rows.length} row(s) selected.
		</div>
		<Button
			variant="outline"
			size="sm"
			on:click={() => ($pageIndex = $pageIndex - 1)}
			disabled={!$hasPreviousPage}>Previous</Button
		>
		<Button
			variant="outline"
			size="sm"
			disabled={!$hasNextPage}
			on:click={() => ($pageIndex = $pageIndex + 1)}>Next</Button
		>
	</div>
</div>
