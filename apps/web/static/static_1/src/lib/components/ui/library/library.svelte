<script lang="ts">
	import { createEventDispatcher } from "svelte";

	import * as Tabs from "$lib/components/ui/tabs";
	import * as Avatar from "$lib/components/ui/avatar";
	import { Input } from "$lib/components/ui/input";
	import { Button } from "$lib/components/ui/button";
	import { crewPresets } from "$lib/dummy-data/crewPresets";
	import { Label } from "$lib/components/ui/label";

	const dispatch = createEventDispatcher();
</script>

<div class="py-4">
	<Tabs.Root value="personal" class="h-screen max-h-[600px]">
		<Tabs.List class="sticky grid w-full grid-cols-2">
			<Tabs.Trigger value="personal">Personal</Tabs.Trigger>
			<Tabs.Trigger value="community">Community</Tabs.Trigger>
		</Tabs.List>
		<Input class="sticky my-6" placeholder="Search..." />
		<Tabs.Content value="personal">
			<ul class="h-full space-y-4 py-6">
				<form
					method="POST"
					class="grid grid-cols-8 rounded-md border border-border bg-card p-6"
					on:submit|preventDefault={async (e) => {
						const file = e.target[0].files[0];

						if (!file) return;

						try {
							const text = await file.text();
							dispatch("crew-load", {
								crew: JSON.parse(text)
							});
						} catch (error) {
							console.error("Error parsing JSON:", error);
						}
					}}
				>
					<div class="col-span-7 grid w-full max-w-sm items-center gap-1.5">
						<Label for="file">Upload a Crew from a file with the button below</Label>

						<Input
							id="file"
							accept=".json"
							type="file"
							class="border border-border bg-foreground/10"
						/>
					</div>
					<div class="col-span-1 ml-auto">
						<Button variant="outline" type="submit">Load</Button>
					</div>
				</form>

				{#each crewPresets as preset}
					<li class="w-full gap-2">
						<div class="grid grid-cols-8 rounded-md border border-border bg-card p-6">
							<Avatar.Root class="mr-auto">
								<Avatar.Image src="https://github.com/shadcn.png" alt="@shadcn" />
								<Avatar.Fallback>CN</Avatar.Fallback>
							</Avatar.Root>
							<div class="col-span-3">
								<h3 class="text-lg font-bold">{preset.instance_id}</h3>
							</div>
							<div class="col-span-3">
								<p>{preset.instance_id}</p>
							</div>
							<div class="col-span-1 ml-auto">
								<Button variant="outline">Load</Button>
							</div>
						</div>
					</li>
				{/each}
			</ul>
		</Tabs.Content>
		<Tabs.Content value="community">COMING SOON!</Tabs.Content>
	</Tabs.Root>
</div>
