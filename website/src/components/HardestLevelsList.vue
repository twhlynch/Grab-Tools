<script lang="ts">
import { downloadLevel } from '@/common/levels';
import CheckmarkIcon from '@/icons/CheckmarkIcon.vue';
import CrossIcon from '@/icons/CrossIcon.vue';
import DownloadIcon from '@/icons/DownloadIcon.vue';
import EditIcon from '@/icons/EditIcon.vue';
import { add_hardest_level_request } from '@/requests/AddHardestLevelRequest';
import { ListRowData } from '@/requests/GetHardestLevelsRequest';
import { remove_hardest_level_request } from '@/requests/RemoveHardestLevelRequest';
import { useUserStore } from '@/stores/user';
import downloads from '@/tools/downloads';
import { mapState } from 'pinia';
import { defineComponent, PropType } from 'vue';

export default defineComponent({
	components: {
		DownloadIcon,
		EditIcon,
		CrossIcon,
		CheckmarkIcon,
	},
	props: {
		list: Array as PropType<ListRowData[]>,
	},
	emits: ['update'],
	data() {
		return {
			edit_level_id: null as string | null,
			remove_level_id: null as string | null,
			edit_level_position: null as number | null,
		};
	},
	computed: {
		...mapState(useUserStore, ['is_logged_in', 'grab_id', 'is_list_moderator']),
	},
	methods: {
		async edit_level(level_id: string) {
			if (this.edit_level_id !== level_id) {
				this.edit_level_id = level_id;
				return;
			}

			if (this.edit_level_position) {
				const success = await add_hardest_level_request(level_id, this.edit_level_position);
				if (success) {
					window.toast(`Updated level`);
					this.$emit('update');
				}
			}

			this.edit_level_id = null;
		},
		async remove_level(level_id: string) {
			if (this.remove_level_id !== level_id) {
				this.remove_level_id = level_id;
				return;
			}

			const success = await remove_hardest_level_request(level_id);
			if (success) {
				window.toast(`Removed level`);
				this.$emit('update');
			}
			this.remove_level_id = null;
		},
		level_url(level_id: string) {
			return this.$config.GRAB_VIEWER_URL + level_id;
		},
		user_class(level_id: string) {
			return this.is_logged_in && this.grab_id === level_id.split(':')[0] && 'personal';
		},
		async download(level_id: string) {
			const level = await downloads.download_level(level_id);
			if (!level) {
				window.toast('Download failed');
				return null;
			}
			downloadLevel(level, level_id);
		},
	},
});
</script>

<template>
	<div>
		<div
			v-for="({ title, creators, level_id, position }, i) in list"
			:key="i"
			:class="['leaderboard-item', 'list-item', user_class(level_id)]"
		>
			<p>{{ position }}</p>
			<a :href="level_url(level_id)" target="_blank">{{ title }}</a>
			<span class="divider" @click="download(level_id)">
				<DownloadIcon class="icon" />
			</span>
			<p v-if="edit_level_id !== level_id">
				{{ creators.split(/[,\s]/)[0] }}
			</p>
			<div v-if="edit_level_id === level_id && is_list_moderator" class="container">
				<input
					v-model="edit_level_position"
					type="number"
					placeholder="Position"
					@keyup.enter="edit_level(level_id)"
				/>
				<button class="btn" @click="edit_level(level_id)">
					<CheckmarkIcon />
				</button>
			</div>
			<div v-if="edit_level_id !== level_id && is_list_moderator" class="container">
				<button class="btn edit" @click="edit_level(level_id)">
					<EditIcon />
				</button>
				<button
					:class="['btn', 'remove', remove_level_id === level_id && 'active']"
					@click="remove_level(level_id)"
				>
					<CrossIcon />
				</button>
			</div>
		</div>
	</div>
</template>

<style scoped>
.divider {
	cursor: pointer;
}
.icon {
	aspect-ratio: auto;
	scale: 80%;
	opacity: 0.8;
}
.container {
	display: flex;
	flex-direction: row;
	gap: 5px;
	padding-left: 10px;

	input {
		padding: 5px 10px;
		background: #2e5d9740;
		border-radius: 5px;
		color: var(--text-color-default);
	}
}
.btn {
	padding-inline: 5px;
	background: transparent;
	cursor: pointer;

	span {
		width: 20px;
	}
	&.active span {
		color: var(--red);
	}
}
</style>
