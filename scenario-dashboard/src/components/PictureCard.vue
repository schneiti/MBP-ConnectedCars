<template>
  <div>
    <img style="max-height: 300px" :src="resolve_img_url(picture_src)" />
    <div class="pic_sub">{{pic_desc}}</div>
  </div>
</template>
<script>
export default {
  name: 'PictureCard',
  props: {
    picture_src: String,
    pic_desc: String
  },
  methods: {
    resolve_img_url: function (path) {
      let images = require.context('../assets/', false, /\.png$|\.jpg$/)
      return images("./"+path)
    }
  }
}
</script>
