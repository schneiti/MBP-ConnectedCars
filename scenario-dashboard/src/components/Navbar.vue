<template>
  <b-navbar toggleable="sm" type="dark" variant="dark">
    <b-navbar-toggle target="nav-text-collapse"></b-navbar-toggle>

    <b-navbar-brand>IoV Scenarios</b-navbar-brand>

    <b-collapse id="nav-text-collapse" is-nav>
      <b-navbar-nav>
        <!-- Navbar dropdowns -->
        <b-nav-item-dropdown text="Connected Cars: MBP" right>
          <b-dropdown-item :to="{name: 'ScenOne' }">Emergency braking warning</b-dropdown-item>
          <b-dropdown-item :to="{name: 'ScenTwo' }">Forward collision warning</b-dropdown-item>
          <b-dropdown-item  :to="{name: 'ScenThree' }">Wrong way driver on a highway</b-dropdown-item>
          <b-dropdown-item :to="{ name: 'ScenFour' }">Obstructed view</b-dropdown-item
          >
        </b-nav-item-dropdown>
      </b-navbar-nav>
      <b-navbar-nav class="ml-auto">
        <b-nav-item right style="color: white">{{ timestamp }}</b-nav-item>
      </b-navbar-nav>
    </b-collapse>
  </b-navbar>
</template>

<script>
export default {
  name: "Navbar",
  data() {
    return {
      timestamp: "",
    };
  },
  methods: {
    getNow: function () {
      const today = new Date();
      const date =
        today.getFullYear() +
        "-" +
        (today.getMonth() + 1) +
        "-" +
        today.getDate();
      const time =
        today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
      const dateTime = date + " " + time;
      this.timestamp = dateTime;
    },
  },
  created() {
    setInterval(this.getNow, 1000);
  },
};
</script>
