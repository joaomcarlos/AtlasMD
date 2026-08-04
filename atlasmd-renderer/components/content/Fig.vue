<template>
    <div class="fig">
        <!-- inline image -->
        <figure>
            <img class="inline-image" :src="refinedInlineSrc" :alt="props.caption"
                :style="{ width: props.width, cursor: props.allowZoom ? 'zoom-in' : 'default' }"
                @click.stop="openModal" />
            <figcaption class="caption" v-if="props.caption">{{ props.caption }}</figcaption>
        </figure>

        <!-- modal image -->
        <div v-if="props.allowZoom && modalIsOpen" class="modal-image-overlay" role="dialog" aria-modal="true"
            @click.stop="closeModal">
            <div class="modal-image-bg" :style="{
                background: props.keepTransparentBg ? 'transparent' : colorMode.preference === 'dark' ? 'rgba(15, 19, 32, 0.95)' : 'rgba(255, 255, 255, 1)'
            }">
                <img class="modal-image" :src="refinedModalSrc" :alt="props.caption" @click.stop="closeModal" />
            </div>


        </div>
    </div>

</template>

<script setup lang="ts">
import { computed, useRuntimeConfig } from '#imports';
import { joinURL, withLeadingSlash, withTrailingSlash } from 'ufo';
import { onBeforeUnmount, onMounted, ref } from 'vue';

const colorMode = useColorMode();

const props = withDefaults(
    defineProps<{
        // dark/light mode image: inline
        src: string
        darkmodeSrc?: string
        caption?: string
        width?: string
        // dark/light mode image: modal
        srcModal?: string
        darkmodeSrcModal?: string
        // misc
        allowZoom?: boolean, // don't want to allow zooming on the inline image?
        keepTransparentBg?: boolean | string // want the modal to have a transparent background color?
    }>(),
    {
        caption: '',
        width: 'auto',
        allowZoom: true,
        keepTransparentBg: false
    }
)

// Convert string "false"/"true" to actual booleans
const keepTransparentBg = computed(() => {
    if (typeof props.keepTransparentBg === 'string') {
        return props.keepTransparentBg === 'true'
    }
    return props.keepTransparentBg
})

const refineSrcURL = (src: string) => {
    if (src?.startsWith('/') && !src.startsWith('//')) {
        const _base = withLeadingSlash(withTrailingSlash(useRuntimeConfig().app.baseURL))
        if (_base !== '/' && !src.startsWith(_base)) {
            return joinURL(_base, src)
        }
    }
    return src
}

const refinedInlineSrc = computed(() => {
    let src = colorMode.preference === 'light' ? props.src : props.darkmodeSrc ?? props.src
    return refineSrcURL(src)
})

const refinedModalSrc = computed(() => {
    // if there's no modal use the light mode src
    const lightModeSrcModal = props.srcModal ?? props.src
    // if theres no darkmode modal use the darkmode src or fallback to light mode modal
    const darkModeSrcModal = props.darkmodeSrcModal ?? props.darkmodeSrc ?? lightModeSrcModal
    let src = colorMode.preference === 'light' ? lightModeSrcModal : darkModeSrcModal
    return refineSrcURL(src)
})

console.debug('src', refinedInlineSrc.value)
console.debug('modalSrc', refinedModalSrc.value)
console.debug('caption', props.caption)
console.debug('width', props.width)
console.debug('keepTransparentBg', props.keepTransparentBg)

// handle modal
const modalIsOpen = ref(false)
const openModal = () => modalIsOpen.value = true
const closeModal = () => modalIsOpen.value = false

const onKeydown = (e: KeyboardEvent) => {
    if (e.key === 'Escape' && modalIsOpen.value) { closeModal() }
}
onMounted(() => {
    window.addEventListener('keydown', onKeydown)
})
onBeforeUnmount(() => {
    window.removeEventListener('keydown', onKeydown)
})


</script>

<style scoped>
.fig {
    position: relative;
    display: block;
    width: 100%;
}

/* inline */
.inline-image {
    transition: transform 0.2s ease;
    border-radius: 8px;
}

.inline-image:hover {
    transform: scale(1.02);
}


/* modal */
.modal-image {
    cursor: zoom-out;
    width: 100%;
    max-width: 95vw;
    max-height: 95vh;
    object-fit: contain;
}

.modal-image-overlay {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.6);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
    padding: 2rem;
}

.modal-image-bg {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    max-width: 100%;

    border-radius: 8px;
}
</style>


<!--
How to use:

1. Simplest use case

::fig
---
src: /path/to/the/light/mode/image
---
::

2. With caption and width

::fig
---
src: /path/to/the/light/mode/image
caption: "Image caption"
width: "600px"
---
::

3. With dark mode image

::fig
---
src: /path/to/the/light/mode/image
darkmodeSrc: /path/to/the/dark/mode/image
---
::

4. With dark mode image + different zoom images

::fig
---
src: /path/to/the/light/mode/image
srcModal: /path/to/the/light/mode/modal/image
darkmodeSrc: /path/to/the/dark/mode/image
darkmodeSrcModal: /path/to/the/dark/mode/modal/image
---
::

5. Don't allow zooming

::fig
---
src: /path/to/the/light/mode/image
allowZoom: false
---
::


-->
