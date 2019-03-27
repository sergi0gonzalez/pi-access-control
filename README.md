# PI - Multi-method access control 
In the control of access to a building it is normal that there is a verification of the identity of a person. These verification can be made by a human or by a machine. The latter frees a human agent from the tedious (and error prone) task of identifying people (often relying on memory) and register them in and out. Authenticating people should be flexible, in order to attain personal preferences and avoid discontentment, without, relaxing the level of confidence implicit in the authentication process.
The purpose of this work is to conceive, realize, and experiment a prototype of a multi-method authentication portic using different kinds of hardware.

## System Requirements
As result of the first phase of the prototype development, we present in this section a brief system requirements specification.

### Requirements Elicitation

#### Actors
 * [System Administrator] - Person in charge with credential administration, logs verification, grant/revoke permissions

 * [Security Agent] - Person in charge of register the people in and out, who is allowed to enter the building, should be sitting at the front desk, and have access to the security dashboard.

 * [IEETA Personnel] - Teachers, researchers and staff who should be granted access to the building

 * [Visitor] - Any person who desires access to the building, this may either be university staff, students, researchers. This actor may or may not already have a UA universal user.

#### Use Cases

Sequence of actions, related to the building access, using a Mobile App or a Smart Card (Citizens Card)
![alt text](https://raw.githubusercontent.com/sergi0gonzalez/pi-access-control/master/images/MobileAppSeq.png)

#### Non-functional requirements
 * [Security]

 * [Usability]

 * [Integrability]

 * [Scalability]

 * [Portability]

## System Architecture

### Domain Model

Entities, Roles and Relationships of the system
![alt_text](https://raw.githubusercontent.com/sergi0gonzalez/pi-access-control/master/images/DomainModel.png)

### Physical Model

Physical architecture of the system
![alt text](https://raw.githubusercontent.com/sergi0gonzalez/pi-access-control/master/images/PhysicalModel.png)

### Technological Model

Technologies of the system
![alt text](https://raw.githubusercontent.com/sergi0gonzalez/pi-access-control/master/images/TechnologicalModel.png)
