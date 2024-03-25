<script lang="ts">
	import { SplitTest } from 'svelte-split-testing';
	import { Toaster } from '$lib/components/ui/sonner';
	import FormItem from '$lib/components/FormItem.svelte';
	import type { ActionData, PageData } from './$types';
	import SEO from '$lib/components/SEO/index.svelte';
	import { Logo } from '$lib/components/ui/logo';
	import * as Tabs from '$lib/components/ui/tabs';
	import * as Card from '$lib/components/ui/card';
	import { Button } from '$lib/components/ui/button';
	import { Input } from '$lib/components/ui/input';
	import { Label } from '$lib/components/ui/label';
	import PricingTiers from '$lib/components/pricing/PricingTiers.svelte';
	import { faqList as faqs } from '$lib/faq-data';
	import { fade } from 'svelte/transition';
	import { Codesandbox, Gauge, HeartHandshake, Key, Settings2, Waves } from 'lucide-svelte';

	export let form: ActionData;

	export let data: PageData;
	const titleVariants = {
		'0': 'Join the Future of AI<br /> with Exclusive Early Access to <span class="bg-gradient-to-b from-primary to-background from-50% bg-clip-text text-transparent">Aitino</span>'
		// '1': 'Create Solutions Like <br /> Never Before with <span class="bg-gradient-to-r from-primary to-danger bg-clip-text text-transparent">Aitino</span>',
		// '2': 'Automate Your Business <br /> with <span class="bg-gradient-to-r from-primary to-danger bg-clip-text text-transparent">Aitino</span>',
		// '3': 'Create teams of  AI Agents <br/> to solve any task.',
		// '4': 'Join the Multi-Agent <br/> Revolution with <span class="bg-gradient-to-r from-primary to-danger bg-clip-text text-transparent">Aitino</span>',
		// '5': 'Join the Future of AI with <br/>  Exclusive Early Access to <span class="bg-gradient-to-r from-primary to-danger bg-clip-text text-transparent">Aitino</span>',
		// '6': 'Create Solutions Like <br/>  Never Before with <span class="bg-gradient-to-r from-primary to-danger bg-clip-text text-transparent">Aitino</span>',
		// '7': 'Automate Your Business <br/>  with <span class="bg-gradient-to-r from-primary to-danger bg-clip-text text-transparent">Aitino</span>'
	};

	const subtitleVariants: Record<string, string> = {
		'0': "Aitino is a platform that allows for the creation of teams of AI Agents to help you automate tasks and solve complex problems. It's made easily customizable through a node-editor."
	};

	let selectedIndex: number = 0;

	const features = [
		{
			title: 'Teams of AI Agents',
			description:
				'Harness the collective intelligence of AI teams designed to collaborate and amplify problem-solving capabilities. Experience the synergy of multiple AI agents working in concert to tackle complex tasks efficiently.',
			image: '/screenshots/crew_1_no_user_prompt.png'
		},
		{
			title: 'Fully Custom Agents',
			description:
				'Tailor your AI agents to meet your unique needs with fully customizable solutions. Create agents that align perfectly with your workflow and specific challenges.',
			image: '/screenshots/agent_node_horizontal_1.png'
		},
		{
			title: 'Community Libraries',
			description:
				'Tap into tons of assets from community-driven libraries, where shared insights fuel innovation. Benefit from a repository of resources that grows smarter through collective contributions.',
			image: ''
		},
		{
			title: 'Multi-modal Task Solving',
			description:
				"Address a diverse range of problems with AI agents capable of multi-modal task solving. Whether it's text, image, or data-centric challenges, our versatile agents adapt to deliver results.",
			image: ''
		}
	];

	const benefits = [
		{
			title: 'Complex Problem Solving',
			description:
				"Navigate through intricate challenges with AI Crews, designed for high-level task solving through collaboration, broadening the horizon of what's achievable.",
			icon: Key
		},
		{
			title: 'Rapid Prototyping',
			description:
				'Accelerate the development of innovative ideas with Aitino, enabling users to quickly prototype solutions through AI-driven analyses and agent collaboration.',
			icon: Gauge
		},
		{
			title: 'Streamlined Operations',
			description:
				'Automate complex workflows with ease, reducing manual effort and increasing productivity.',
			icon: Waves
		},
		{
			title: 'Enhanced Creativity',
			description:
				"Unlock new potentials in content creation, powered by AI's versatility in handling diverse tasks and data types.",
			icon: Codesandbox
		},
		{
			title: 'Community Support',
			description:
				'Benefit from collective intelligence by leveraging the hours of work of other users through shared assets.',
			icon: HeartHandshake
		},
		{
			title: 'Customization at Core',
			description:
				'Tailor every aspect of your AI agents to fit exact business needs, ensuring maximum effectiveness and integration.',
			icon: Settings2
		}
	];

	function selectFeature(index: number) {
		selectedIndex = index;
	}
</script>

<Toaster />

<svelte:head>
	<script type="text/javascript">
		window.$crisp = [];
		window.CRISP_WEBSITE_ID = 'd8b6e215-1bae-470a-b3c4-0e227902e47a';
		(function () {
			d = document;
			s = d.createElement('script');
			s.src = 'https://client.crisp.chat/l.js';
			s.async = 1;
			rel = 'preconnect';
			d.getElementsByTagName('head')[0].appendChild(s);
		})();
	</script>
</svelte:head>

<SEO
	slug="early-access"
	title="Aitino - Create AI Crews"
	metadescription="Create a Crew of AI Agents with Aitino - The world's leading web platform in pairing modern AI Agents with communication abililities. By taking the form of node-editors, Aitino harnesses the ability to create teams of AI agents that collaborate to solve complex tasks in real-time."
/>
<main class="relative overflow-hidden">
	<div
		class="pointer-events-none absolute h-[50000px] w-full bg-inherit bg-[linear-gradient(to_right,#80808012_1px,transparent_1px),linear-gradient(to_bottom,#80808012_1px,transparent_1px)] bg-[size:150px_150px]"
	></div>
	<section class="relative flex h-screen w-screen flex-col justify-center">
		<div class="flex w-screen flex-col justify-evenly py-6 md:mt-24 lg:mt-28 xl:mt-32">
			<div
				class="mx-auto flex w-full flex-col place-items-center gap-y-4 px-2 text-foreground sm:gap-y-8"
			>
				<Logo height="h-16" class="hidden rounded-xl lg:flex" />
				<h1
					class="tracking-loose m-0 text-center text-3xl font-semibold sm:m-0 sm:text-5xl md:text-6xl lg:text-6xl xl:text-7xl"
				>
					<SplitTest key="Title Test" variants={Object.keys(titleVariants)} let:variant>
						{@html titleVariants[0]}
					</SplitTest>
				</h1>

				<h3
					class="m-0 mx-auto mt-2 max-w-3xl text-balance text-center text-sm text-foreground brightness-75 sm:m-0 sm:text-lg md:text-lg lg:text-xl xl:text-2xl"
				>
					<SplitTest key="Subtitle Test" variants={Object.keys(subtitleVariants)} let:variant>
						{@html subtitleVariants[variant]}
					</SplitTest>
				</h3>

				<FormItem mainform={form} notform={data} />
			</div>
		</div>
	</section>

	<section
		id="features-section"
		aria-label="Features for running your books"
		class="relative overflow-hidden pb-28 pt-20 sm:py-32"
	>
		<div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
			<div class="mb-8 max-w-2xl md:mx-auto md:text-center xl:max-w-none">
				<h2 class="text-3xl font-semibold tracking-tight text-foreground sm:text-4xl md:text-5xl">
					Become a more efficient entrepreneur
				</h2>
				<p class="mt-6 text-lg tracking-tight text-foreground/80">
					Here's a list of Aitino's features that will save you time and money.
				</p>
			</div>

			<Tabs.Root value="0" class="">
				<Tabs.List class="grid w-full grid-cols-4">
					{#each features as feature, value}
						<Tabs.Trigger value={value.toString()}>{feature.title}</Tabs.Trigger>
					{/each}
				</Tabs.List>
				{#each features as feature, value}
					<Tabs.Content value={value.toString()}>
						<Card.Root class="p-8">
							<Card.Header class="text-center">
								<Card.Title class="text-3xl">{feature.title}</Card.Title>
								<Card.Description class="text-md mx-auto max-w-xl text-balance">
									<p transition:fade>{feature.description}</p>
								</Card.Description>
							</Card.Header>
							<Card.Content class="space-y-2">
								<div class="mx-auto w-full max-w-3xl rounded-xl border border-border">
									{#if feature.image != ''}
										<img
											class="w-full rounded-xl object-cover"
											src={feature.image}
											alt="screenshot of the feature of {feature.title}"
										/>
									{:else}
										<div class="mx-auto max-w-7xl px-6 py-16 sm:py-24 lg:px-8">
											<h2
												class="text-center text-3xl font-semibold uppercase tracking-tight text-accent sm:text-4xl md:text-5xl"
											>
												Coming Soon
											</h2>
										</div>
									{/if}
								</div>
							</Card.Content>
						</Card.Root>
					</Tabs.Content>
				{/each}
			</Tabs.Root>
		</div>
	</section>

	<section class=" py-24 sm:py-32" id="benefits-section">
		<div class="mx-auto max-w-7xl px-6 lg:px-8">
			<div class="mx-auto max-w-2xl sm:text-center">
				<h2 class="text-base font-semibold leading-7 text-primary">Everything you need</h2>
				<p class="mt-2 text-3xl font-bold tracking-tight text-white sm:text-4xl">
					Not VC backed? Not a problem.
				</p>
				<p class="mt-6 text-lg leading-8 text-gray-300">
					Solve, Prototype, and Automate with Your Own Crews
				</p>
			</div>
		</div>
		<div class="relative overflow-hidden pt-16">
			<div class="mx-auto max-w-7xl px-6 lg:px-8">
				<img
					src="/screenshots/crew_editor_1.png"
					alt="App screenshot"
					class="mb-[-12%] rounded-xl shadow-2xl ring-1 ring-white/10"
					width="2432"
					height="1442"
				/>
				<div class="relative" aria-hidden="true">
					<div
						class="absolute -inset-x-1 bottom-0 bg-gradient-to-t from-primary-900/20 pt-[7%]"
					></div>
				</div>
			</div>
		</div>
		<div class="mx-auto mt-16 max-w-7xl px-6 sm:mt-20 md:mt-24 lg:px-8">
			<dl
				class="mx-auto grid max-w-2xl grid-cols-1 gap-x-6 gap-y-10 text-base leading-7 text-foreground/75 sm:grid-cols-2 lg:mx-0 lg:max-w-none lg:grid-cols-3 lg:gap-x-8 lg:gap-y-16"
			>
				{#each benefits as { title, description, icon }}
					<div class="relative pl-9">
						<dt class="inline font-semibold text-foreground">
							<svelte:component this={icon} class="absolute left-1 top-1 h-5 w-5 text-primary" />
							{title}.
						</dt>
						<dd class="inline">
							{description}
						</dd>
					</div>
				{/each}
			</dl>
		</div>
	</section>

	<section id="pricing-section">
		<div class="mx-auto max-w-7xl px-4 py-12 sm:px-6 sm:py-24 md:px-8 md:py-32">
			<div class="mb-8 max-w-3xl md:mx-auto md:text-center xl:max-w-none">
				<h2
					class="tracking-loose m-0 text-balance text-center text-3xl font-semibold sm:m-0 sm:text-5xl md:text-6xl lg:text-6xl"
				>
					Flexible plans for versatile problems
				</h2>
			</div>
			<PricingTiers />
		</div>
	</section>

	<section>
		<div class="mx-auto max-w-7xl px-6 py-16 sm:py-24 lg:px-8">
			<h2 class="text-3xl font-semibold tracking-tight text-foreground sm:text-4xl md:text-5xl">
				Frequently asked questions
			</h2>
			<p class="mt-6 max-w-2xl text-base leading-7 text-foreground/75">
				Have a different question and can’t find the answer you’re looking for? Reach out to us by <a
					href="mailto:contact@futi.no"
					class="font-semibold text-accent hover:text-accent-700">sending us an email</a
				> and we’ll get back to you as soon as we can.
			</p>
			<div class="mt-20">
				<dl
					class="space-y-16 sm:grid sm:grid-cols-2 sm:gap-x-6 sm:gap-y-16 sm:space-y-0 lg:grid-cols-3 lg:gap-x-10"
				>
					{#each faqs as { question, answer }}
						<div>
							<dt class="text-balance text-lg font-semibold text-foreground">
								{question}
							</dt>
							<dd class="leading- mt-2 text-pretty text-sm text-foreground/75">
								{@html answer}
							</dd>
						</div>
					{/each}
				</dl>
			</div>
		</div>
	</section>
</main>
