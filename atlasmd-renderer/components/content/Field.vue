<template>
    <div class="field">
        <div class="field-meta">
            <span class="field-name">{{ props.name }}</span>
            <span class="field-type">({{ props.type }})</span>
            <span class="field-required" v-if="props.required">*</span>
            <span>:</span>
        </div>
        <div class="field-description">
            <slot v-if="$slots.description" name="description" />
            <slot v-else />
        </div>
    </div>
    <!-- possible extra payload subfields -->
    <div v-if="$slots.subfields" class="subfields">
        <slot name="subfields" />
    </div>
</template>

<script setup lang="ts">

const props = defineProps({
    name: { type: String, required: true },
    type: { type: String, required: true },
    required: { type: Boolean, default: false }
})

</script>

<style scoped lang="ts">
css({
    '.field': {
        display: 'flex',
        alignItems: 'baseline',
        gap: '{space.1}',
        marginBottom: '{space.3}',
    },
    '.field-meta': {
        display: 'flex',
        alignItems: 'center',
        gap: '{space.1}',
    },
    '.field-name': {
        fontWeight: '600',
        fontSize: '{fontSize.sm}',
        color: '{color.gray.900}',
        '@dark': {
            color: '{color.gray.100}',
        },
    },
    '.field-type': {
        fontSize: '{fontSize.xs}',
        color: '{color.gray.500}',
        '@dark': {
            color: '{color.gray.400}',
        },
    },
    '.field-required': {
        fontWeight: 'bold',
        color: '{color.red.600}',
        '@dark': {
            color: '{color.red.400}',
        },
    },
    '.field-description :deep(p)': {
        // override default p styles anywhere inside the field-description
        fontSize: '{fontSize.sm}',
        margin: '0',
    },
    '.field-description': {
        fontStyle: 'italic',
        color: '{color.primary.600}',
        '@dark': {
            color: '{color.primary.300}',
        },
    },
    '.subfields': {
        paddingLeft: '{space.3}',
        borderLeft: '2px solid',
        borderColor: '{color.gray.200}',
        '@dark': {
            borderColor: '{color.primary.600}',
        },
    },
})
</style>
