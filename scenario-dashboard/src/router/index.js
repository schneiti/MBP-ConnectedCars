import Vue from "vue";
import Router from "vue-router";
import NotFound from "@/components/NotFound";
import ScenOne from "@/components/ScenOne";
import ScenTwo from "@/components/ScenTwo";
import ScenThree from "@/components/ScenThree";
import ScenFour from "@/components/ScenFour";

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: "/",
      name: "ScenOne",
      component: ScenOne,
    },
    {
      path: "/ScenOne",
      name: "ScenOne",
      component: ScenOne,
    },
    {
      path: "/ScenTwo",
      name: "ScenTwo",
      component: ScenTwo,
    },
    {
      path: "/ScenThree",
      name: "ScenThree",
      component: ScenThree,
    },
    {
      path: "/ScenFour",
      name: "ScenFour",
      component: ScenFour,
    },
    {
      path: "*",
      name: "NotFound",
      component: NotFound,
    },
  ],
});
