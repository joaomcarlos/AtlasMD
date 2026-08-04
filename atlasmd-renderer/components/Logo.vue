<template>
  <div class="flex-center">
    <!-- check if it's dark or light mode and set a different logo accordingly-->
    <span v-if="colorMode.preference === 'dark'">
      <img :src="config.public.atlasLogoDark" alt="Logo-Dark-Mode" />
    </span>
    <span v-else-if="colorMode.preference === 'light'">
      <img :src="config.public.atlasLogoLight" alt="Logo-Light-Mode" />
    </span>
    <span v-else>
      <img :src="config.public.atlasLogoDarkBg" alt="Logo-Dark-Mode-BG" />
    </span>

    <div class="flex-center">
      <span class="logo-title">{{ config.public.atlasTitle }}</span>
      <span v-if="config.public.atlasAppVersion" class="chip" style="margin-top: 5px">
        {{config.public.atlasAppVersion}}
      </span>
    </div>
  </div>
</template>

<script setup lang="ts">
const colorMode = useColorMode();
const config = useRuntimeConfig()
</script>


<style scoped lang="ts">
css({
  img: {
    width: '50px',
    height: '50px'
  },
  '.flex-center': {
    display: 'flex',
    alignItems: 'center'
  },
  '.logo-title': {
    marginLeft: '5px',
    marginRight: '5px',
    fontSize: '30px',
    fontWeight: 'bold',
    color: '{color.primary.900}',
    '@dark': {
      color: '{color.white}',
    }
  },
  '.chip': {
    padding: '2px 7px',
    fontSize: '12px',
    borderRadius: '25px',

    color: '{color.white}',
    backgroundColor: '{color.secondary.800}',
    '@dark': {
      color: '{color.white}',
      backgroundColor: '{color.secondary.500}'

    }
  },
})
</style>

<!-- svg only logo with color changing in the middle. need to make the aligning correct  -->
<!-- <template>
  <svg
    width="165"
    height="165"
    xmlns="http://www.w3.org/2000/svg"
    xml:space="preserve"
    version="1.1"
    viewBox="0 0 150 150"
  >
    <g id="svg_7">
      <path
        fill="#E01F26"
        d="m49.4937,44.52501c10.4,-9.2 23.8,-13.5 37.4,-11.9l-0.1,0.5l-1.1,9.4l30.3,-12.8l-26.3,-20l-1.2,9.9c-17.2,-1.9 -34.6,3.6 -47.7,15.2c-25,22.5 -27.1,61.1 -4.6,86.2l9.7,-8.7c-17.6,-19.7 -16,-50 3.6,-67.8z"
        class="st1"
      />
      <path
        fill="#E01F26"
        d="m129.2937,44.57501c-2.6,3.4 -6.2,7.9 -8.3,10.7c15.5,19.6 13.5,48.3 -5.4,65.2c-10.4,9.2 -23.8,13.5 -37.5,11.9l0.1,-0.5l1.2,-9.4l-30.4,12.8l26.3,20l1.3,-9.9c17.2,1.9 34.7,-3.6 47.7,-15.2c24.8,-22.2 26.9,-60.5 5,-85.6z"
        class="st1"
      />
      <path
        fill="currentColor"
        d="m107.6937,82.47501c0,-4.7 -1.3,-9 -3.6,-12.8l7.5,-7.5l-8.3,-8.3l-7.5,7.5c-3.7,-2.3 -8.1,-3.6 -12.7,-3.6c-4.7,0 -9,1.3 -12.7,3.6l-7.5,-7.5l-8.3,8.3l7.5,7.5c-2.3,3.7 -3.6,8.1 -3.6,12.7c0,4.7 1.3,9 3.6,12.7l-7.5,7.5l8.3,8.3l7.5,-7.5c3.7,2.3 8.1,3.6 12.8,3.6c4.7,0 9,-1.3 12.7,-3.6l7.5,7.5l8.3,-8.3l-7.5,-7.3c2.2,-3.8 3.5,-8.1 3.5,-12.8zm-18.5,14.3c-1.9,0.8 -3.9,1.2 -6,1.2c-2.1,0 -4.2,-0.4 -6,-1.2c-3.7,-1.6 -6.7,-4.6 -8.3,-8.3c-0.8,-1.8 -1.2,-3.9 -1.2,-6c0,-2.1 0.4,-4.2 1.2,-6c1.6,-3.7 4.5,-6.7 8.3,-8.3c1.9,-0.8 3.9,-1.2 6,-1.2c2.1,0 4.2,0.4 6,1.2c3.7,1.6 6.7,4.5 8.3,8.3c0.8,1.9 1.2,3.9 1.2,6c0,2.1 -0.4,4.2 -1.2,6c-1.6,3.7 -4.6,6.7 -8.3,8.3z"
        class="st0"
      />
    </g>
  </svg>
</template>

<style scoped lang="ts">
css({
  svg: {
    fill: '{color.primary}',
    '@dark': {
      fill: '{color.white}'
    }
  }
})
</style> -->
