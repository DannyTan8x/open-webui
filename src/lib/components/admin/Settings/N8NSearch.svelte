<script lang="ts">
	import { getRAGConfig, updateRAGConfig } from '$lib/apis/retrieval';
	import Switch from '$lib/components/common/Switch.svelte';

	import { models } from '$lib/stores';
	import { onMount, getContext } from 'svelte';
	import { toast } from 'svelte-sonner';
	import SensitiveInput from '$lib/components/common/SensitiveInput.svelte';
	import Tooltip from '$lib/components/common/Tooltip.svelte';

	const i18n = getContext('i18n');

	export let saveHandler: Function;

	let webSearchEngines = [
		'searxng',
		'yacy',
		'google_pse',
		'brave',
		'kagi',
		'mojeek',
		'bocha',
		'serpstack',
		'serper',
		'serply',
		'searchapi',
		'serpapi',
		'duckduckgo',
		'tavily',
		'jina',
		'bing',
		'exa',
		'perplexity',
		'sougou',
		'firecrawl',
		'external'
	];

	let n8nConfig = null;

	const submitHandler = async () => {
		// 型別修正前的淺拷貝，避免修改 reactive 的原始 n8nConfig
		const cleanN8nConfig = {
			...n8nConfig,
			N8N_SEARCH_RESULT_COUNT: n8nConfig?.N8N_SEARCH_RESULT_COUNT
				? parseInt(n8nConfig.N8N_SEARCH_RESULT_COUNT)
				: undefined,
			N8N_SEARCH_DOMAIN_FILTER_LIST: Array.isArray(n8nConfig?.N8N_SEARCH_DOMAIN_FILTER_LIST)
				? n8nConfig.N8N_SEARCH_DOMAIN_FILTER_LIST
				: [],
		};

		if (n8nConfig.BYPASS_N8N_EMBEDDING_AND_RETRIEVAL === "")
		n8nConfig.BYPASS_N8N_EMBEDDING_AND_RETRIEVAL = false;

		const res = await updateRAGConfig(localStorage.token, {
			n8n: cleanN8nConfig
		});

		if (res?.status === true) {
			toast.success('Config saved!');
		} else {
			toast.error('Failed to save config');
		}
	};


	onMount(async () => {
		const res = await getRAGConfig(localStorage.token);

		if (res) {
			n8nConfig = res.n8n;
		}
	});
</script>

<form
	class="flex flex-col h-full justify-between space-y-3 text-sm"
	on:submit|preventDefault={async () => {
		await submitHandler();
		saveHandler();
	}}
>
	<div class=" space-y-3 overflow-y-scroll scrollbar-hidden h-full">
		{#if n8nConfig}
			<div class="">
				<div class="mb-3">
					<div class=" mb-2.5 text-base font-medium">{$i18n.t('General')}</div>

					<hr class=" border-gray-100 dark:border-gray-850 my-2" />

					<div class="  mb-2.5 flex w-full justify-between">
						<div class=" self-center text-xs font-medium">
							{$i18n.t('N8N Search')}
						</div>
						<div class="flex items-center relative">
							<Switch bind:state={n8nConfig.ENABLE_N8N_SEARCH} />
						</div>
					</div>
					<div class=" mb-2.5 flex flex-col w-full justify-between">
						<div>
							<div class=" self-center text-xs font-medium mb-1">
								{$i18n.t('N8N API Key')}
							</div>

							<SensitiveInput
								placeholder={$i18n.t('Enter N8N API Key')}
								bind:value={n8nConfig.N8N_API_KEY}
							/>
						</div>
						
					</div>
					
					<div class="  mb-2.5 flex flex-col w-full justify-between">
						<div class=" mb-1 text-xs font-medium">
							{$i18n.t('N8N WEBHOOK URL')}
						</div>
						<div class="flex items-center relative">
							<input
								class="flex-1 w-full rounded-lg text-sm bg-transparent outline-hidden"
								type="text"
								placeholder={$i18n.t('Enter N8N WEBHOOK URL (e.g. http://n8n:5678/webhook/flow)')}
								bind:value={n8nConfig.N8N_WEBHOOK_URL}
								autocomplete="off"
								required
							/>
						</div>
					</div>
					<div class="w-full">
						<div class=" self-center text-xs font-medium mb-1">
							{$i18n.t('Search Result Count')}
						</div>

						<input
							type="number"
							class="w-full rounded-lg py-2 px-4 text-sm bg-gray-50 dark:text-gray-300 dark:bg-gray-850 outline-hidden"
							placeholder={$i18n.t('Search Result Count')}
							bind:value={n8nConfig.N8N_SEARCH_RESULT_COUNT}
							required
						/>
					</div>

					<div class="  mb-2.5 flex w-full justify-between">
						<div class=" self-center text-xs font-medium">
							<Tooltip content={$i18n.t('Bypass Embedding and Retrieval')} placement="top-start">
								{$i18n.t('Bypass Embedding and Retrieval')}
							</Tooltip>
						</div>
						<div class="flex items-center relative">
							<Tooltip content={''}>
								<Switch bind:state={n8nConfig.BYPASS_N8N_EMBEDDING_AND_RETRIEVAL} />
							</Tooltip>
						</div>
					</div>

				</div>
			</div>
		{/if}
	</div>
	<div class="flex justify-end pt-3 text-sm font-medium">
		<button
			class="px-3.5 py-1.5 text-sm font-medium bg-black hover:bg-gray-900 text-white dark:bg-white dark:text-black dark:hover:bg-gray-100 transition rounded-full"
			type="submit"
		>
			{$i18n.t('Save')}
		</button>
	</div>
</form>
