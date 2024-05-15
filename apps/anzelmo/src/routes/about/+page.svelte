<script>
	import Header from '$lib/components/organisms/Header.svelte';
</script>

<Header />
<main class="text-left flex gap-x-4 mx-6 mt-16 md:mx-8 lg:mx-28 h-screen items-center">
	<div class="grid grid-cols-1 md:grid-cols-2 h-screen items-center gap-x-4 lg:gap-x-8 py-10">
		<div class=" md:py-16 lg:py-8 max-h-screen h-full w-full flex items-center">
			<!--Temp. div; will be portrait of Mr. Anzelmo.-->
			<img
				src="/temp_photography/photo1.jpg"
				alt=""
				class="bg-surface-variant w-full object-no-repeat object-center object-cover h-[500px] sm:h-[600px] md:h-full" />
		</div>
		<div class="flex flex-col py-12 md:px-6 md:py-24 lg:py-32 max-w-xl lg:mx-auto">
			<h1 class="display-small py-2 uppercase">About</h1>
			<p class="body-large py-2 tracking-wide leading-relaxed md:leading-loose">
				Lorem ipsum dolor sit amet, consectetur adipisicing elit. Earum, consequuntur, esse ex
				deleniti repellat illo temporibus saepe est odit laboriosam ad non reprehenderit aut ullam
				commodi fugit, dolor iure dolores natus debitis facilis tempore.
			</p>
			<div class="flex flex-col my-4 py-4 border-t border-outline">
				<h1 class="title-large py-2 uppercase">Socials</h1>
				<ul
					class="flex flex-col gap-y-2 text-tertiary underline underline-offset-2 md:no-underline tracking-wide">
					<li>
						<a
							class="hover:text-tertiary underline-animation"
							href="#">
							Instagram
						</a>
					</li>
					<li>
						<a
							class="hover:text-tertiary underline-animation"
							href="#">
							Facebook
						</a>
					</li>
					<li>
						<a
							class="hover:text-tertiary underline-animation"
							href="#">
							Email
						</a>
					</li>
				</ul>
			</div>
		</div>
	</div>
</main>
