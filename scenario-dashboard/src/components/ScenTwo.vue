<template>
  <HelloWorld scenName="scen2" header="Scenario: Forward collision warning at an instersection" 
  overview="#### Overview
   
Two cars are driving at high speed towards an intersection where a left-before-right right-of-way rule applies. If they maintained their speed without properly looking out for each other, a collision would occur. To prevent this, a cloud component evaluates the car data in real time and detects the collision. Collision warnings are issued to both cars and the car without right of way is requested to reduce its speed so that it arrives at the intersection with a delay."
  img="scen2.png"/>
</template>

<script>
import HelloWorld from "@/components/HelloWorld.vue";

export default {
  name: 'ScenTwo',
  components: {
    HelloWorld,
  },
};
</script>
