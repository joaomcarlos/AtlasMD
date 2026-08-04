<!--
use in .md file like:

::example-component
---
foo: FOOO
:items: '["item1", "item2"]'
---
This text will be shown at the end of the component, after the title and description.

#title
This is just an example component

#description
This is a description of the example component.
::

or like this:

::example-component{foo='foo' :items='["item1", "item2"]'}
This text will be shown at the end of the component, after the title and description.

#title
This is just an example component

#description
This is a description of the example component.
::

-->

<template>
    <h2 class="title">
        <slot name="title" mdc-unwrap="p" />
    </h2>

    <div>
        <p>Args:</p>
        <p>
            <strong>foo:</strong> {{ props.foo }}<br />
            <strong>bar:</strong> {{ props.bar }}

            <span v-for="item in props.items" :key="item">
                <br />
                <strong>item:</strong> {{ item }}
            </span>
        </p>
    </div>

    <span v-if="$slots.description" class="description">
        <slot name="description" mdc-unwrap="p" />
    </span>

    <slot />

</template>

<script setup lang="ts">

const props = defineProps({
    foo: { type: String, required: true },
    bar: { type: String, default: 'baz' },
    items: { type: Array<string>, default: () => [] }
})

console.debug('props.foo', props.foo)
console.debug('props.bar', props.bar)
console.debug('props.items', props.items, typeof props.items)
</script>


<style scoped>
.title {
    color: red;
}

.description {
    color: blue;
    font-style: italic;
}
</style>
