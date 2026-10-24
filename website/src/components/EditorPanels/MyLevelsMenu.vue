<script lang="ts">
import { decodeLevel } from '@/common/levels';
import GeneralPopup from '@/components/GeneralPopup.vue';
import RefreshedIcon from '@/icons/RefreshedIcon.vue';
import { user_levels_request } from '@/requests/UserLevelsRequest';
import { useUserStore } from '@/stores/user';
import downloads from '@/tools/downloads';
import { LevelDetails } from '@grab-tools/lib/data/types';
import { mapState } from 'pinia';
import { defineComponent } from 'vue';

export default defineComponent({
	components: {
		GeneralPopup,
		RefreshedIcon,
	},
	props: {
		visible: {
			type: Boolean,
			required: true,
		},
	},
	emits: ['update:visible', 'open', 'insert'],
	data() {
		return {
			levels: [] as LevelDetails[],
			state: 'idle',
			loading: false,
			search: '',
		};
	},
	computed: {
		...mapState(useUserStore, ['is_logged_in', 'grab_id']),
		filtered_levels() {
			const query = this.search.trim().toLowerCase();
			if (!query) return this.levels;
			return this.levels.filter(
				(level) =>
					(level.title ?? '').toLowerCase().includes(query) ||
					level.identifier.toLowerCase().includes(query),
			);
		},
	},
	watch: {
		visible(value: boolean) {
			if (value) void this.load(true);
		},
	},
	methods: {
		async load(force = false) {
			if (!this.is_logged_in || !this.grab_id) return;
			if (this.loading) return;
			if (this.state === 'loaded' && !force) return;

			const first_load = this.state !== 'loaded';
			if (first_load) this.state = 'loading';

			this.loading = true;
			const levels = await user_levels_request(this.grab_id);
			this.loading = false;

			if (!levels) {
				if (first_load) this.state = 'error';
				return;
			}
			this.levels = levels;
			this.state = 'loaded';
		},
		async load_level(level: LevelDetails) {
			const data = await downloads.try_download_level(level.identifier);
			if (!data) return null;

			const blob = new Blob([data], {
				type: 'application/octet-stream',
			});
			return await decodeLevel(blob);
		},
		async open(level: LevelDetails) {
			const json = await this.load_level(level);
			if (!json) return;
			this.$emit('open', json);
			this.$emit('update:visible', false);
		},
		async insert(level: LevelDetails) {
			const json = await this.load_level(level);
			if (!json) return;
			this.$emit('insert', json);
		},
	},
});
</script>

<template>
	<GeneralPopup :visible="visible" @update:visible="$emit('update:visible', $event)">
		<div class="header">
			<span>My Levels</span>
			<button
				v-if="is_logged_in && grab_id"
				class="refresh"
				title="Refresh"
				:disabled="loading"
				@click="
					() => {
						load(true);
					}
				"
			>
				<RefreshedIcon class="refresh-icon" :class="{ busy: loading }" />
			</button>
		</div>
		<div v-if="!is_logged_in" class="status">Log in to view your levels</div>
		<div v-else-if="!grab_id" class="status">Verify your account to view your levels</div>
		<template v-else>
			<input v-model="search" class="search" type="text" placeholder="Search levels..." />
			<div v-if="state === 'loading'" class="status">Loading...</div>
			<div v-else-if="state === 'error'" class="status">
				<span>Failed to load levels</span>
				<button
					class="retry"
					@click="
						() => {
							load(true);
						}
					"
				>
					Retry
				</button>
			</div>
			<div v-else-if="!filtered_levels.length" class="status">
				{{ search ? 'No matching levels' : 'No levels found' }}
			</div>
			<div v-else class="levels">
				<div v-for="level of filtered_levels" :key="level.identifier" class="level">
					<span class="title" :title="level.identifier">
						{{ level.title || level.identifier }}
					</span>
					<button
						class="insert"
						@click="
							() => {
								insert(level);
							}
						"
					>
						Insert
					</button>
					<button
						class="open"
						@click="
							() => {
								open(level);
							}
						"
					>
						Open
					</button>
				</div>
			</div>
		</template>
	</GeneralPopup>
</template>

<style scoped>
.header {
	display: flex;
	flex-direction: row;
	justify-content: space-between;
	align-items: center;
	padding-inline: 0.5rem;
}
.header button,
.retry {
	width: auto;
	height: 1.6rem;
	line-height: 1.6rem;
	padding-inline: 0.8rem;
	border-radius: 0.8rem;
}
.refresh-icon {
	width: 1.2rem;
	height: 1.2rem;
}
.refresh-icon.busy {
	animation: spin 1s linear infinite;
}
@keyframes spin {
	from {
		transform: rotate(0deg);
	}
	to {
		transform: rotate(360deg);
	}
}
.search {
	height: 2rem;
	box-sizing: border-box;
	padding-inline: 0.8rem;
	border: none;
	border-radius: 1rem;
	background-color: #2e2e2e;
	color: white;
	outline: none;
}
.status {
	text-align: center;
	opacity: 0.7;
	display: flex;
	flex-direction: row;
	gap: 0.5rem;
	align-items: center;
	justify-content: center;
}
.levels {
	display: flex;
	flex-direction: column;
	gap: 0.5rem;
	overflow-y: auto;
	max-height: 60vh;
}
.level {
	align-items: center;
	display: flex;
	flex-direction: row;
	gap: 0.5rem;
	padding-inline: 0.5rem;
}
.title {
	word-break: break-word;
	margin-right: auto;
}
.level button {
	width: auto;
	height: 1.6rem;
	line-height: 1.6rem;
	padding-inline: 0.8rem;
	border-radius: 0.8rem;
}
</style>
