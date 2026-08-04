<template>
    <div class="card" :style="props.style">
        <slot />
    </div>
</template>

<script setup lang="ts">

const props = defineProps({
    style: {
        type: Object,
        default: () => ({}),
        description: 'Custom styles for the card'
    }
})

</script>


<style scoped lang="ts">
css({
    '.card': {
        fontSize: '{fontSize.sm}',
        paddingTop: '{space.3}',
        paddingBottom: '{space.1}',
        paddingLeft: '{space.3}',
        marginTop: '{space.3}',
        marginBottom: '{space.3}',
        marginLeft: '0',
        marginRight: '{space.3}',
        boxShadow: '0 1px 2px 0 rgba(0,0,0,0.03)',
        border: '1px solid',
        borderRadius: '{radii.md}',
        borderColor: '{color.gray.200}',
        background: '{color.gray.50}',
        '@dark': {
            borderColor: '{color.primary.700}',
            background: '{color.primary.800}',
        },
    }
})
</style>
