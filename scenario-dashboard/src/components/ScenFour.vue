<template>
  <HelloWorld scenName="scen4" header="Scenario: Obstructed view" 
  overview="### Overview
  
  At a T-junction, a car and a truck want to turn side by side. However, the truck has driven a little further ahead than the car, which is why Car1 can no longer see the oncoming traffic in its target lane. Therefore, the car asks for camera data from the camera side of the truck on the right side in order to be able to see the oncoming traffic and to turn without losing time, which would occur if the car first had to wait for the truck to turn."
  img="scen4.png"/>
</template>

<script>
import HelloWorld from "@/components/HelloWorld.vue";

export default {
  name: 'ScenFour',
  components: {
    HelloWorld,
  },
};
</script>
