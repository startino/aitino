<script lang="ts">
	import { SplitTest } from 'svelte-split-testing';
	import { Toaster } from '$lib/components/ui/sonner';
	import { Button } from '$lib/components/ui/button';
	import { Github, Youtube } from 'lucide-svelte';
	import SEO from '$lib/components/SEO/index.svelte';
	import { Logo } from '$lib/components/ui/logo';
	import * as Tabs from '$lib/components/ui/tabs';
	import * as Card from '$lib/components/ui/card';
	import PricingTiers from '$lib/components/pricing/PricingTiers.svelte';
	import { faqList as faqs } from '$lib/faq-data';
	import { fade } from 'svelte/transition';
	import { Codesandbox, Gauge, HeartHandshake, Key, Settings2, Waves } from 'lucide-svelte';

	export let form;

	export let data;

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

				<div class="grid w-full max-w-lg grid-cols-2 gap-4">
					<Button class="p-8 text-xl" href="/app">Try for Free</Button>
					<Button class="p-8 text-xl" variant="outline" href="mailto:contact@futi.no"
						>Contact Us</Button
					>
				</div>

				<div
					class="mx-auto mt-2 flex h-fit w-fit flex-wrap-reverse items-center justify-between gap-2 sm:flex-row md:p-4 lg:mt-6 xl:mt-12"
				>
					<Button
						class="bg-transparent p-6 font-bold text-accent transition-all duration-300 ease-in-out hover:scale-95 hover:bg-primary hover:text-primary-foreground "
						href="https://github.com/Futino/"
						target="_blank"
					>
						<Github size="34" />
						<div class="flex flex-col py-4">
							<p class="px-4 py-4 text-base">
								Github
								<br />
								@futino
							</p>
						</div>
					</Button>

					<Button
						class="bg-transparent p-6 font-bold text-accent transition-all duration-300 ease-in-out hover:scale-95 hover:bg-primary hover:text-primary-foreground"
						href="https://www.youtube.com/@futinolimited"
						target="_blank"
					>
						<Youtube size="34" />
						<div class="flex flex-col">
							<p class="px-4 py-4 text-base">
								Youtube
								<br />
								@futino
							</p>
						</div>
					</Button>
					<Button
						class="bg-transparent p-6 font-bold text-accent transition-all duration-300 ease-in-out hover:scale-95 hover:bg-primary hover:text-primary-foreground"
						href="https://discord.gg/6M3dSFnufV"
						target="_blank"
					>
						<svg
							fill="currentColor"
							stroke="currentColor"
							viewBox="0 0 32 32"
							width="34"
							height="34"
							xmlns="http://www.w3.org/2000/svg"
							><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g
								id="SVGRepo_tracerCarrier"
								stroke-linecap="round"
								stroke-linejoin="round"
							></g><g id="SVGRepo_iconCarrier"
								><path
									d="M 12.65625 4.90625 L 11.875 5 C 11.875 5 8.371094 5.382813 5.8125 7.4375 L 5.78125 7.4375 L 5.75 7.46875 C 5.175781 7.996094 4.925781 8.644531 4.53125 9.59375 C 4.136719 10.542969 3.714844 11.753906 3.34375 13.09375 C 2.601563 15.777344 2 19.027344 2 22 L 2 22.25 L 2.125 22.5 C 3.050781 24.125 4.695313 25.160156 6.21875 25.875 C 7.742188 26.589844 9.058594 26.96875 9.96875 27 L 10.5625 27.03125 L 10.875 26.5 L 11.96875 24.5625 C 13.128906 24.824219 14.464844 25 16 25 C 17.535156 25 18.871094 24.824219 20.03125 24.5625 L 21.125 26.5 L 21.4375 27.03125 L 22.03125 27 C 22.941406 26.96875 24.257813 26.589844 25.78125 25.875 C 27.304688 25.160156 28.949219 24.125 29.875 22.5 L 30 22.25 L 30 22 C 30 19.027344 29.398438 15.777344 28.65625 13.09375 C 28.285156 11.753906 27.863281 10.542969 27.46875 9.59375 C 27.074219 8.644531 26.824219 7.996094 26.25 7.46875 L 26.21875 7.4375 L 26.1875 7.4375 C 23.628906 5.382813 20.125 5 20.125 5 L 19.34375 4.90625 L 19.0625 5.625 C 19.0625 5.625 18.773438 6.355469 18.59375 7.1875 C 17.460938 7.035156 16.535156 7 16 7 C 15.464844 7 14.539063 7.035156 13.40625 7.1875 C 13.226563 6.355469 12.9375 5.625 12.9375 5.625 Z M 11.28125 7.1875 C 11.324219 7.328125 11.367188 7.449219 11.40625 7.5625 C 10.113281 7.882813 8.734375 8.371094 7.46875 9.15625 L 8.53125 10.84375 C 11.125 9.234375 14.851563 9 16 9 C 17.148438 9 20.875 9.234375 23.46875 10.84375 L 24.53125 9.15625 C 23.265625 8.371094 21.886719 7.882813 20.59375 7.5625 C 20.632813 7.449219 20.675781 7.328125 20.71875 7.1875 C 21.652344 7.375 23.433594 7.804688 24.90625 8.96875 C 24.898438 8.972656 25.28125 9.550781 25.625 10.375 C 25.976563 11.222656 26.367188 12.351563 26.71875 13.625 C 27.394531 16.066406 27.925781 19.039063 27.96875 21.65625 C 27.339844 22.617188 26.171875 23.484375 24.9375 24.0625 C 23.859375 24.566406 23.007813 24.75 22.5 24.84375 L 22 24 C 22.296875 23.890625 22.589844 23.769531 22.84375 23.65625 C 24.382813 22.980469 25.21875 22.25 25.21875 22.25 L 23.90625 20.75 C 23.90625 20.75 23.34375 21.265625 22.03125 21.84375 C 20.71875 22.421875 18.714844 23 16 23 C 13.285156 23 11.28125 22.421875 9.96875 21.84375 C 8.65625 21.265625 8.09375 20.75 8.09375 20.75 L 6.78125 22.25 C 6.78125 22.25 7.617188 22.980469 9.15625 23.65625 C 9.410156 23.769531 9.703125 23.890625 10 24 L 9.5 24.84375 C 8.992188 24.75 8.140625 24.566406 7.0625 24.0625 C 5.828125 23.484375 4.660156 22.617188 4.03125 21.65625 C 4.074219 19.039063 4.605469 16.066406 5.28125 13.625 C 5.632813 12.351563 6.023438 11.222656 6.375 10.375 C 6.71875 9.550781 7.101563 8.972656 7.09375 8.96875 C 8.566406 7.804688 10.347656 7.375 11.28125 7.1875 Z M 12.5 14 C 11.726563 14 11.042969 14.441406 10.625 15 C 10.207031 15.558594 10 16.246094 10 17 C 10 17.753906 10.207031 18.441406 10.625 19 C 11.042969 19.558594 11.726563 20 12.5 20 C 13.273438 20 13.957031 19.558594 14.375 19 C 14.792969 18.441406 15 17.753906 15 17 C 15 16.246094 14.792969 15.558594 14.375 15 C 13.957031 14.441406 13.273438 14 12.5 14 Z M 19.5 14 C 18.726563 14 18.042969 14.441406 17.625 15 C 17.207031 15.558594 17 16.246094 17 17 C 17 17.753906 17.207031 18.441406 17.625 19 C 18.042969 19.558594 18.726563 20 19.5 20 C 20.273438 20 20.957031 19.558594 21.375 19 C 21.792969 18.441406 22 17.753906 22 17 C 22 16.246094 21.792969 15.558594 21.375 15 C 20.957031 14.441406 20.273438 14 19.5 14 Z M 12.5 16 C 12.554688 16 12.625 16.019531 12.75 16.1875 C 12.875 16.355469 13 16.648438 13 17 C 13 17.351563 12.875 17.644531 12.75 17.8125 C 12.625 17.980469 12.554688 18 12.5 18 C 12.445313 18 12.375 17.980469 12.25 17.8125 C 12.125 17.644531 12 17.351563 12 17 C 12 16.648438 12.125 16.355469 12.25 16.1875 C 12.375 16.019531 12.445313 16 12.5 16 Z M 19.5 16 C 19.554688 16 19.625 16.019531 19.75 16.1875 C 19.875 16.355469 20 16.648438 20 17 C 20 17.351563 19.875 17.644531 19.75 17.8125 C 19.625 17.980469 19.554688 18 19.5 18 C 19.445313 18 19.375 17.980469 19.25 17.8125 C 19.125 17.644531 19 17.351563 19 17 C 19 16.648438 19.125 16.355469 19.25 16.1875 C 19.375 16.019531 19.445313 16 19.5 16 Z"
								></path></g
							></svg
						>
						<div class="flex flex-col">
							<p class="px-4 py-4 text-base">
								Discord
								<br />
								Aitino
							</p>
						</div>
					</Button>
				</div>
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
