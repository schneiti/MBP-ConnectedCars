<template>
  <HelloWorld scenName="scen3" header="Scenario: Wrong way driver on a  highway" 
  overview="### Overview
  
  A car takes the wrong exit from a motorway service station and does not realise that it is entering the motorway from the opposite direction. Fortunately, the car is connected to the IoV, allowing a central system or individual cars on the motorway to detect this hazardous situation. In response, all cars on the motorway section are directed to the right lane and slowed down if necessary so that the wrong-way car can safely drive in the remaining lanes until the next exit (entry to this exit is not covered by the scenario data). The right lane is chosen by the other cars because most road users are used to driving on the right and changing to other lanes could take too much time and cause traffic congestion especially for many trucks."
  img="scen3.png"/>
</template>

<script>
import HelloWorld from "@/components/HelloWorld.vue";

export default {
  name: 'ScenThree',
  components: {
    HelloWorld,
  },
};
</script>
