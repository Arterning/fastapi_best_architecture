import { defineStore } from 'pinia';
import { DocState } from './types';

const useDocStore = defineStore('docStore', {
    state: () : DocState => ({
        query: undefined,
        starQuery: undefined,
        personQuery: undefined,
        orgQuery: undefined,
    }),

    getters: {
        getState(state: DocState): DocState {
            return {...state }
        },
    },

    actions: {
        setState(partial: Partial<DocState>) {
            this.$patch(partial);
        },
    }
});

export default useDocStore;