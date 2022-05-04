<template>
  <div class="hello">
    <b-card
      header="Scenario Documentation"
      header-tag="header"
      footer-tag="footer"
    >
      <div style="max-height=100px; overflow-y: auto;">
        <h2 style="text-align: left">
          {{ header }}
        </h2>
        <PictureCard  v-bind:picture_src="img" pic_desc=''/>
        <div v-html="compiledMarkdown" style="text-align: left"></div>
      </div>
    </b-card>
    <div>
      <b-card-group deck style="margin-top: 30px">
        <b-card
          header="Actuator Control"
          header-tag="header"
          footer-tag="footer"
        >
          <table>
            <tr>
              <td>
                <b-form inline>
                  <b-button @click="deploy">Deploy</b-button>

                  <b-button @click="getDeployStatus">Status update</b-button>
                </b-form>
              </td>
              <td>
                <b-form inline>
                  <b-input-group
                    prepend="hh:mm:ss"
                    class="mb-2 mr-sm-2 mb-sm-0"
                  >
                    <b-form-input
                      id="inline-form-input-username"
                      placeholder="Start time (GMT)"
                      v-model="startTime"
                    ></b-form-input>
                  </b-input-group>
                  <b-button variant="success" @click="start">▶ Start</b-button>
                  <b-button variant="danger" @click="stopAllPolling"
                    >⏹ Stop</b-button
                  >
                </b-form>
              </td>
            </tr>
          </table>

          <div>
            <b-table
              style="margin-top: 30px"
              :busy="busyStatusActuatorTable"
              striped
              hover
              :items="actuatorControlItems"
              :sticky-header="true"
              :no-border-collapse="false"
            >
              <template #table-busy>
                <div class="text-center text-danger my-2">
                  <b-spinner class="align-middle"></b-spinner>
                  <strong>Loading...</strong>
                </div>
              </template></b-table
            >
          </div>

          <p style="text-align: center">
            {{ deployment_status.data.status }}
          </p>
        </b-card>

        <b-card header="Actuator Message Event Log">
          <div>
            <b-table
              striped
              hoverc
              :items="eventItems"
              :sticky-header="true"
              :no-border-collapse="false"
            >
            </b-table>
            <b-button
              style="text-align: left"
              variant="danger"
              @click="clearEventTable"
              >Clear table</b-button
            >
          </div>
        </b-card>
      </b-card-group>
    </div>
    <b-card header="Scenario Live Map" style="margin-top: 30px">
      <div id="map"></div>
    </b-card>

    <b-card header="ValueLog Display" style="margin-top: 30px">
      <div>
        <b-table
          striped
          hover
          :items="valueLogsDisplayTableData"
          :sticky-header="true"
          :no-border-collapse="false"
        >
        </b-table>
      </div>
    </b-card>
  </div>
</template>

<script>
import "leaflet/dist/leaflet.css";
import L from "leaflet";
import axios from "axios";
import { marked } from "marked";
import PictureCard from "./PictureCard.vue";


delete L.Icon.Default.prototype._getIconUrl;

L.Icon.Default.mergeOptions({
  iconRetinaUrl: require("leaflet/dist/images/marker-icon-2x.png"),
  iconUrl: require("leaflet/dist/images/marker-icon.png"),
  shadowUrl: require("leaflet/dist/images/marker-shadow.png"),
});

export default {
  name: "HelloWorld",
  props: {
    header: String,
    scenName: String,
    overview: String,
    img: String,
  },
  data() {
    return {
      markdown: this.overview,
      actuatorControlItems: [
        { iov_object_name: "Not known", id: "Not known", status: "Not known" },
      ],
      eventItems: [
        {
          Time: "-",
          From: "-",
          To: "-",
          Msg: "-",
        },
      ],
      busyStatusActuatorTable: false,
      eventTableWaitForNewEvents: false,
      polling_status: null,
      polling_valueLogs: null,
      polling_deploy_status: null,
      deployment_status: { data: { status: "unknown" } },
      valueLogs: { data: { CAR_1: "", CAR_2: "", CAR_3: "" } },
      valueLogsDisplayTableData: [
        {
          Name: "-",
          Time: "-",
          ScenarioTime: "-",
          LastMsgRcvd: "-",
          Latitude: "-",
          Longitude: "-",
          Bearing: "-",
          Velocity: "-",
          Acceleration: "-",
        },
      ],
      startTime: "",
      center: [37, 7749, -122, 4194],
      allPoints: [],
      timestamp: "",
    };
  },
   components: {
      PictureCard
  },
  computed: {
    compiledMarkdown: function () {
      return marked(this.markdown, { sanitize: true });
    },
  },

  methods: {
    stopPolling: function () {
      clearInterval(this.polling_status);
      clearInterval(this.polling_deploy_status);
    },

    stopAllPolling: function () {
      this.stopPolling();
      clearInterval(this.polling_valueLogs);
    },

    pollStatus: function () {
      this.polling_status = setInterval(() => {
        this.checkStatus();
      }, 1000);
    },

    pollValueLog: function () {
      this.polling_valueLogs = setInterval(() => {
        this.getLastValueLog();
      }, 1000);
    },

    pollDeployStatus: function () {
      this.polling_deploy_status = setInterval(() => {
        this.getDeployStatus();
      }, 5000);
    },

    deploy: function () {
      axios.post(
        "http://localhost:8000/deploy?scenario_name=" + this.scenName
      );
      this.pollStatus();
      //this.pollDeployStatus();
    },

    start: function () {
      this.stopPolling();
      axios.post(
        "http://localhost:8000/start?start_time=" +
          this.startTime +
          "&scenario_name=" +
          this.scenName
      );
      this.pollValueLog();
      this.eventItems = [
        {
          Time: "-",
          From: "-",
          To: "-",
          Msg: "-",
        },
      ];
    },

    clearEventTable: function () {
      this.eventItems = [
        {
          Time: "-",
          From: "-",
          To: "-",
          Msg: "-",
        },
      ];
    },

    checkStatus: function () {
      axios
        .get("http://localhost:8000/status?scenario_name=" + this.scenName)
        .then((response) => (this.deployment_status = response));
    },

    onMsgEvent(time, event) {
      // Add a new table entry if the msg isn't already in the event msg table
      var append = true;
      for (var i = 0; i < this.eventItems.length; i++) {
        if (this.eventItems[i].Msg == event.msg) {
          append = false;
        }
      }
      if (append) {
        if (this.eventItems.length == 1 && this.eventItems[0].Time == "-") {
          this.eventItems.shift();
        }

        var newEventObjToAdd = {
          Time: time,
          From: event.from,
          To: event.to,
          Msg: event.msg,
        };
        this.eventItems.push(newEventObjToAdd);
      }
    },

    /**
     *
     */
    displayValueLogs: function () {
      let coordsList = [];

      if (!("data" in this.valueLogs) || this.valueLogs.data.length <= 0) {
        return;
      }

      let data = this.valueLogs.data;

      let newTableData = [];

      // Message transformations for the gui views
      for (const car of data) {
        let valueLog = car.values.content[0].value;

        newTableData.push({
          Name: car.name,
          Time: this.convertUnixTimeToReadableTimeStr(
            car.values.content[0].time
          ),
          ScenarioTime: valueLog.scenario_meta.time,
          LastMsgRcvd: valueLog.scenario_meta.last_message_received,
          Latitude: valueLog.position.latitude,
          Longitude: valueLog.position.longitude,
          Bearing: valueLog.position.bearing,
          Velocity:
            "" +
            valueLog.motion.speed.speed_val +
            valueLog.motion.speed.speed_unit,
          Acceleration:
            "" +
            valueLog.motion.acceleration.acc_val +
            valueLog.motion.acceleration.acc_unit,
        });

        let singlePointCoords = [
          valueLog.position.latitude,
          valueLog.position.longitude,
        ];
        coordsList.push(singlePointCoords);

        if (valueLog.scenario_meta.last_message_received != "no_message") {
          this.onMsgEvent(
            valueLog.scenario_meta.time,
            JSON.parse(valueLog.scenario_meta.last_message_received)
          );
        }
      }

      // Apply valuelog changes to table
      this.valueLogsDisplayTableData = newTableData;

      if (coordsList.length > 0) {
        this.updateData(coordsList);
      }
    },

    getDeployStatus: function () {
      this.busyStatusActuatorTable = true;
      axios
        .get(
          "http://localhost:8000/deploy-status?scenario_name=" +
            this.scenName
        )
        .then((response) => {
          this.actuatorControlItems = response.data;
          this.busyStatusActuatorTable = false;
        });
    },

    getLastValueLog: function () {
      axios
        .get(
          "http://localhost:8000/value-log?scenario_name=" + this.scenName
        )
        .then((response) => {
          this.valueLogs = response;
          this.displayValueLogs();
        });

      // Visualize the value log
      this.removeAllPoints();
    },

    setupLeafletMap: function () {
      this.map = L.map("map").setView([51.505, -0.09], 13);
      L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution:
          '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
      }).addTo(this.map);

      this.markers = [];
    },

    updateData: function (coordsList) {
      if (this.allPoints.length <= 0) {
        this.removeAllPoints();
        this.displayNewMapData(coordsList);
        return;
      }
      this.setPositionOfMarkersnew(coordsList);
    },

    displayNewMapData: function (coordsList) {
      this.allPoints.push(coordsList);

      for (var i = 0; i < coordsList.length; i++) {
        var littleton = L.marker(coordsList[i])
          .bindPopup(coordsList[i].toString())
          .addTo(this.map);
        this.markers.push(littleton);
      }

      this.map.fitBounds([coordsList]);
    },

    setPositionOfMarkersnew: function (newCoordsList) {
      var initialMarkerLength = this.markers.length;
      for (var i = 0; i < initialMarkerLength; i++) {
        var newLatLng = new L.LatLng(newCoordsList[i][0], newCoordsList[i][1]);
        this.markers[i].setLatLng(newLatLng);
      }
    },

    removeAllPoints: function () {
      var initialMarkerLength = this.markers.length;
      for (var i = 0; i < initialMarkerLength; i++) {
        this.map.removeLayer(this.markers.pop());
      }

      this.allPoints.pop();
      if (this.allPoints.length > 0) {
        this.map.fitBounds([this.allPoints]);
      }
    },

    convertUnixTimeToReadableTimeStr(unixTimestamp) {
      // Create a new JavaScript Date object based on the timestamp
      // multiplied by 1000 so that the argument is in milliseconds, not seconds.
      var date = new Date(unixTimestamp * 1000);
      // Hours part from the timestamp
      var hours = date.getHours();
      // Minutes part from the timestamp
      var minutes = "0" + date.getMinutes();
      // Seconds part from the timestamp
      var seconds = "0" + date.getSeconds();

      // Will display time in 10:30:23 format
      var formattedTime =
        hours + ":" + minutes.substr(-2) + ":" + seconds.substr(-2);

      return formattedTime;
    },
  },
  mounted() {
    this.setupLeafletMap();
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
#map {
  height: 500px;
}

button {
  margin: 5px;
}

img {
  text-align: left;
}
</style>
