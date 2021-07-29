package de.ipvs.as.mbp.service.discovery.engine.tasks.template;

import de.ipvs.as.mbp.DynamicBeanProvider;
import de.ipvs.as.mbp.domain.discovery.collections.CandidateDevicesResult;
import de.ipvs.as.mbp.domain.discovery.deployment.DynamicDeployment;
import de.ipvs.as.mbp.domain.discovery.deployment.log.DiscoveryLog;
import de.ipvs.as.mbp.domain.discovery.deployment.log.DiscoveryLogMessage;
import de.ipvs.as.mbp.domain.discovery.deployment.log.DiscoveryLogMessageType;
import de.ipvs.as.mbp.domain.discovery.device.DeviceTemplate;
import de.ipvs.as.mbp.repository.discovery.CandidateDevicesRepository;
import de.ipvs.as.mbp.repository.discovery.DynamicDeploymentRepository;
import de.ipvs.as.mbp.service.discovery.gateway.DiscoveryGateway;

import static de.ipvs.as.mbp.domain.discovery.deployment.log.DiscoveryLogMessageType.INFO;
import static de.ipvs.as.mbp.domain.discovery.deployment.log.DiscoveryLogMessageType.SUCCESS;

/**
 * This task is responsible for checking whether the {@link CandidateDevicesResult} that is stored for a
 * certain {@link DeviceTemplate} is currently used by any {@link DynamicDeployment}s because they are deployed to a
 * device. If this is not the case, this task takes care of deleting the {@link CandidateDevicesResult} and
 * cancelling the subscriptions for asynchronous notifications at the individual discovery repositories.
 */
public class DeleteCandidateDevicesTask implements CandidateDevicesTask {

    //The device template to update the candidate devices for
    private DeviceTemplate deviceTemplate;

    //The discovery log to extend for further log messages
    private DiscoveryLog discoveryLog;

    /*
    Injected fields
     */
    private final DiscoveryGateway discoveryGateway;
    private final CandidateDevicesRepository candidateDevicesRepository;

    /**
     * Creates a new {@link DeleteCandidateDevicesTask} from a given {@link DeviceTemplate}, a force flag and a
     * {@link DiscoveryLog}.
     *
     * @param deviceTemplate The device template to use
     * @param discoveryLog   The {@link DiscoveryLog} to use for logging within this task
     */
    public DeleteCandidateDevicesTask(DeviceTemplate deviceTemplate, DiscoveryLog discoveryLog) {
        //Set fields
        setDeviceTemplate(deviceTemplate);
        setDiscoveryLog(discoveryLog);

        //Inject components
        this.discoveryGateway = DynamicBeanProvider.get(DiscoveryGateway.class);
        this.candidateDevicesRepository = DynamicBeanProvider.get(CandidateDevicesRepository.class);
    }

    /**
     * Implements the actual operations of the task. It is recommended to check for Thread interruptions in order to
     * gracefully deal with cancellations of the task.
     */
    @Override
    public void run() {
        //Write log
        addLogMessage(String.format("Started task for device template \"%s\".", deviceTemplate.getName()));
        addLogMessage("Deleting candidate devices.");

        //Delete the candidate devices
        this.candidateDevicesRepository.deleteById(getDeviceTemplateId());

        //Check whether a subscription exists
        if (!this.discoveryGateway.isSubscribed(deviceTemplate)) {
            //Write log
            addLogMessage(SUCCESS, "Completed successfully.");
            return;
        }

        //Write log
        addLogMessage("Cancelling existing subscription at the discovery repositories.");

        //Send message to discovery repositories in order to cancel the subscriptions
        this.discoveryGateway.cancelSubscription(deviceTemplate);

        //Write log
        addLogMessage(SUCCESS, "Completed successfully.");
    }

    /**
     * Creates a new {@link DiscoveryLogMessage} from a given message string and adds it to the
     * {@link DiscoveryLog} that collects the logs of this task.
     *
     * @param message The actual log message
     */
    private void addLogMessage(String message) {
        //Delegate call
        addLogMessage(INFO, message);
    }

    /**
     * Creates a new {@link DiscoveryLogMessage} from a given message string and a {@link DiscoveryLogMessageType}
     * and adds it to the {@link DiscoveryLog} that collects the logs of this task.
     *
     * @param type    The type of the log message
     * @param message The actual log message
     */
    private void addLogMessage(DiscoveryLogMessageType type, String message) {
        //Check if log messages are supposed to be collected
        if (this.discoveryLog == null) return;

        //Update start timestamp when this is the first log message
        if (discoveryLog.isEmpty()) discoveryLog.updateStartTimestamp();

        //Create new log message
        DiscoveryLogMessage logMessage = new DiscoveryLogMessage(type, message);

        //Add the message to the discovery log of this task
        discoveryLog.addMessage(logMessage);
    }

    /**
     * Returns the device template of this task.
     *
     * @return The device template
     */
    public DeviceTemplate getDeviceTemplate() {
        return this.deviceTemplate;
    }

    /**
     * Sets the device template of this task.
     *
     * @param deviceTemplate The device template to set
     * @return The task
     */
    public DeleteCandidateDevicesTask setDeviceTemplate(DeviceTemplate deviceTemplate) {
        //Null check
        if (deviceTemplate == null) {
            throw new IllegalArgumentException("The device template must not be null.");
        }

        this.deviceTemplate = deviceTemplate;
        return this;
    }

    /**
     * Returns the {@link DiscoveryLog} that is used within this task in order to collect
     * {@link DiscoveryLogMessage}s for logging purposes. May be null, if the task does not perform logging.
     *
     * @return The {@link DiscoveryLog} or null, if logging is not performed
     */
    @Override
    public DiscoveryLog getDiscoveryLog() {
        return discoveryLog;
    }

    /**
     * Sets the {@link DiscoveryLog} that is supposed to be used within this task in order to collect
     * {@link DiscoveryLogMessage}s for logging purposes. If set to null, logging is not formed.
     *
     * @param discoveryLog The {@link DiscoveryLog} or null, if no logging is supposed to be performed
     */
    private void setDiscoveryLog(DiscoveryLog discoveryLog) {
        this.discoveryLog = discoveryLog;
    }

    /**
     * Returns the ID of the {@link DeviceTemplate} on which this task operates.
     *
     * @return The ID of the device template
     */
    @Override
    public String getDeviceTemplateId() {
        return this.deviceTemplate.getId();
    }

    /**
     * Returns a simple, short and human-readable description of the task.
     *
     * @return The human-readable description
     */
    @Override
    public String toHumanReadableString() {
        return "[Delete candidate devices]";
    }
}
