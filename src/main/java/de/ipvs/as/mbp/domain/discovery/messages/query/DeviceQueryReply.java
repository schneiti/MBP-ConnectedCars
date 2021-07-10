package de.ipvs.as.mbp.domain.discovery.messages.query;

import de.ipvs.as.mbp.domain.discovery.description.DeviceDescription;
import de.ipvs.as.mbp.service.messaging.message.DomainMessageBody;
import de.ipvs.as.mbp.service.messaging.message.DomainMessageTemplate;

import java.util.List;

/**
 * Reply message that is supposed to be received in response to {@link DeviceQueryRequest} messages. It contains
 * all the device descriptions of the replying repository that matched the preceding request. This message may be
 * either received in a synchronous manner as direct response to {@link DeviceQueryRequest}s or as asynchronous
 * notification about changes in the repository's result set as part of a subscription. In the latter case,
 * a reference ID is provided that matches the reference ID of the {@link RepositorySubscriptionDetails} object that
 * was part of the {@link DeviceQueryRequest}.
 */
@DomainMessageTemplate(value = "device_query_reply")
public class DeviceQueryReply extends DomainMessageBody {
    //Reference ID matching the one that was provided in the subscription details (if needed)
    private String referenceId;

    //List of device descriptions that matched the query
    private List<DeviceDescription> deviceDescriptions;

    /**
     * Creates a new device query reply.
     */
    public DeviceQueryReply() {

    }

    /**
     * Returns the reference ID or null, if none is provided.
     *
     * @return The reference ID
     */
    public String getReferenceId() {
        return referenceId;
    }

    /**
     * Returns the list of device descriptions that matched the query.
     *
     * @return The list of device descriptions
     */
    public List<DeviceDescription> getDeviceDescriptions() {
        return deviceDescriptions;
    }
}