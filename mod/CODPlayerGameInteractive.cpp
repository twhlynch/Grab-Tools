//
//  CODPlayerGameInteractive.cpp
//  Grab
//
//  Copyright 2017 by Überpixel. All rights reserved.
//  Unauthorized use is punishable by torture, mutilation, and vivisection.
//

#include "CODPlayerGameInteractive.h"
#include "CODWorld.h"
#include "CODPlayedLevelRequest.h"

#define MAX_SPEED_PUSHING 500.0f
#define MAX_SPEED_FROM_OTHER_PLAYER 10.0f
#define MAX_WALK_SPEED 15.0f
#define BOUNCE_SPEED_FACTOR 0.9f

#define HEAD_COLLIDER_RADIUS 0.07f
#define HEAD_COLLIDER_HEIGHT 0.001f

namespace COD
{
	RNDefineMeta(PlayerGameInteractive, PlayerGame)

	PlayerGameInteractive::PlayerGameInteractive(RN::uint16 id, RN::Vector3 position, RN::Quaternion rotation) : PlayerGame(id, position, rotation, true), _controller(nullptr), _rotateTimer(0.0f), _activeHand(-1), _lastHandTriggerValue{ 0.0f, 0.0f }, _didHandLetGo{ false, false }, _twoHandedGrabTimer(0.0f), _rampJumpTimer(0.0f), _isOnGround(false), _groundCollisionType(0), _isAirJumping(false), _isJumpingUp(false), _isSliding(false), _isSlidingUp(false), _isBlockedAbove(false), _isFeetBounce(false), _isBackToEditingPressed(true), _dampingFactor(0.0f), _groundLevelNode(nullptr), _playerWalkDistanceForNextStepSound(0.0f), _didPlayGetupSound(false), _slopeCorrection(0.0f), _wasTriggerPressed{false, false}, _isCheckpointButtonPressed(false), _isRespawnButtonPressed(true) //true to prevent switching back to edit mode in the editor just after switching to play mode
	{
		SetWorldRotation(RN::Quaternion()); //Player class will set the world rotation, but for the interactive player it should always be identity
		_wantsRespawn = true;
		
		//Collision thingy
		RN::PhysXMaterial *controllerMaterial = new RN::PhysXMaterial();
		_controller = new RN::PhysXKinematicController(HEAD_COLLIDER_RADIUS, HEAD_COLLIDER_HEIGHT, controllerMaterial->Autorelease(), 0.01f);
		_controller->SetCollisionFilter(Types::CollisionType::CollisionLocalPlayer, Types::CollisionType::CollisionLevel);
		AddAttachment(_controller);

		_controller->SetContactCallback([&](RN::PhysXCollisionObject *other, const RN::PhysXContactInfo &contact, RN::PhysXCollisionObject::ContactState state) {
			//Trigger level node action if player head is touching it
			LevelNode *levelNode = SafeRetain(other->GetParent()->Downcast<LevelNode>());
			if(levelNode)
			{
				levelNode->Trigger();
				levelNode->Release();
			}
			
			if(contact.normal.y < -0.00001) _isBlockedAbove = true; //Check if the collider is above the player, used to not keep bouncing the player down while trying to get up, epsilonfloat is too small for this
			RNDebug("Impact - isOnGround: " << (_isOnGround? "true" : "false") << ", isBlockedAbove: " << (_isBlockedAbove? "true" : "false") << ", normal: " << contact.normal.y);
			
			//Kill player if head is touching lava
			if(other->GetCollisionFilterGroup() == Types::CollisionLevelLava || other->GetCollisionFilterGroup() == Types::CollisionLevelGrapplableLava)
			{
				PlayDeathSound(true);
				Respawn();
			}
			else if(other->GetCollisionFilterGroup() == Types::CollisionLevelBouncing && !(_isOnGround && _isBlockedAbove))
			{
				if(_speed.GetDotProduct(contact.normal) > 0.0f) return; //early out if already moving away from the collider
				
				RNDebug("Impact - Bounce: (" << _speed.x << ", " << _speed.y << ", " << _speed.z << ")");
				
				RN::Vector3 euler = _head->GetWorldRotation().GetEulerAngle();
				euler.x *= -1.0;
				euler.y = 0.0;
				euler.z = 0.0;
				
				PlayBounceSound(-contact.normal.GetDotProduct(_previousSpeed), RN::Quaternion(euler).GetRotatedVector(contact.position - _controller->GetWorldPosition()).GetNormalized());
				
				//Bounce off bouncing blocks only reducing the speed a bit
				_speed = _speed - contact.normal * _speed.GetDotProduct(contact.normal) * 2.0f;
				_speed *= BOUNCE_SPEED_FACTOR;
			}
			else if(!_isFeetBounce) //Otherwise it cancels the bounce speed out if both, feet and head impact with something in the same update
			{
				if(_speed.GetDotProduct(contact.normal) >= -RN::k::EpsilonFloat && !_isOnGround) return; //early out if already moving away from the collider, but only if feet are not on the ground, to not break the cannon glitch
				
				RNDebug("Impact - Crash");
				
				//Player crashed into a wall and should hear a sound for it
				RN::Vector3 euler = _head->GetWorldRotation().GetEulerAngle();
				euler.x *= -1.0;
				euler.y = 0.0;
				euler.z = 0.0;
				PlayImpactSound(-contact.normal.GetDotProduct(_previousSpeed), RN::Quaternion(euler).GetRotatedVector(contact.position - _controller->GetWorldPosition()).GetNormalized());
				
				_speed -= contact.normal*contact.normal.GetDotProduct(_speed);
			}
		});
		
		_head->AddFlags(RN::SceneNode::Flags::Hidden);

		World *world = World::GetSharedInstance();
		RN::VRCamera *vrCamera = world->GetVRCamera();
		RN::Camera *headCamera = world->GetHeadCamera();
		if(vrCamera)
		{
			_previousHeadPosition = vrCamera->GetHead()->GetPosition();
			RN::Vector3 headPositionOffset = _previousHeadPosition;
			//The spawn position is always on the ground, except when editing and switching to playmode
			if(world->GetServerLevel() != World::ServerLevelEditor && world->GetServerSettings().status != World::ServerStatusTesting)
			{
				headPositionOffset.y = 0.0f;
			}
			vrCamera->SetWorldPosition(GetWorldPosition() - rotation.GetRotatedVector(headPositionOffset));
			vrCamera->SetWorldRotation(rotation);
			vrCamera->SetWorldScale(RN::Vector3(1.0f, 1.0f, 1.0f));
			
			SetWorldPosition(vrCamera->GetHead()->GetWorldPosition());

			RN::Camera *previewCamera = world->GetPreviewCamera();
			if(previewCamera)
			{
				previewCamera->AddChild(_head);
			}
			else
			{
				vrCamera->GetHead()->AddChild(_head);
			}
			
			//feet placement
			_feet->SetPosition(RN::Vector3(0.0f, std::min(-vrCamera->GetHead()->GetPosition().y, 0.0f), 0.0f));
			
			//Hand placement
			RN::VRControllerTrackingState leftHandController = vrCamera->GetControllerTrackingState(0);
			RN::VRControllerTrackingState rightHandController = vrCamera->GetControllerTrackingState(1);
			
			RN::Vector3 controllerPosition[2];
			controllerPosition[0] = vrCamera->GetWorldPosition() - GetWorldPosition() + leftHandController.positionGrip;
			controllerPosition[1] = vrCamera->GetWorldPosition() - GetWorldPosition() + rightHandController.positionGrip;
			
			_hand[0]->SetPosition(controllerPosition[0]);
			_hand[0]->SetRotation(leftHandController.rotationAim);

			_hand[1]->SetPosition(controllerPosition[1]);
			_hand[1]->SetRotation(rightHandController.rotationAim);
			
			//Body rotation
			UpdateBody(0.0f);
		}
		else if(headCamera)
		{
			headCamera->SetWorldPosition(GetWorldPosition() + RN::Vector3(0.0f, 1.6f, 0.0f));
			RN::Vector3 finishPosition = world->GetLevelManager().GetFinishPosition() + RN::Vector3(0.0f, 1.6f, 0.0f);
			headCamera->SetWorldRotation(RN::Quaternion::WithLookAt(headCamera->GetWorldPosition() - finishPosition));
		}
	}
	
	PlayerGameInteractive::~PlayerGameInteractive()
	{
		SafeRelease(_controller);
		_head->RemoveFromParent();
		
		SafeRelease(_groundLevelNode);
	}
	
	void PlayerGameInteractive::Update(float delta)
	{
		//Early out if about to be deleted to prevent some unwanted behavior of them still being alive for another frame
		if(_isScheduledForDeletion) return;
		
		World *world = World::GetSharedInstance();
		RN::VRCamera *vrCamera = world->GetVRCamera();
		if(!vrCamera)
		{
			if(RN::InputManager::GetSharedInstance()->IsControlToggling(RNCSTR("L")))
			{
				RN::PhysXContactInfo contact = world->GetPhysicsWorld()->CastRay(GetWorldPosition(), GetWorldPosition() + GetForward() * 100.0f, Types::CollisionLevel);
				if(contact.distance > 0.0f && contact.node && contact.node->IsKindOfClass(LevelNode::GetMetaClass()))
				{
					LevelNode *contactNode = contact.node->Downcast<LevelNode>();
					RN::Vector3 resultPosition = contactNode->GetWorldPosition() + contactNode->GetWorldRotation().GetRotatedVector(contactNode->GetWorldRotation().GetConjugated().GetRotatedVector(contact.normal) * contactNode->GetScale()) * 0.5f + contact.normal * 0.001;
					RNDebug("Menu position: (" << resultPosition.x << ", " << resultPosition.y << ", " << resultPosition.z << ")");
					
					RN::Quaternion resultRotation = RN::Quaternion::WithLookAt(contact.normal.GetNormalized(), RN::Vector3(0.0f, 1.0f, 0.0f), true);
					RN::Vector3 resultEulerRotation = resultRotation.GetEulerAngle();
					RNDebug("Menu rotation: (" << resultEulerRotation.x << ", " << resultEulerRotation.y << ", " << resultEulerRotation.z << ")");
				}
			}
			
			//P to test push to talk / push to mute
			PlayerSettings *playerSettings = world->GetPlayerSettings(world->GetClientID());
			playerSettings->SetIsPushToTalkButtonPressed(RN::InputManager::GetSharedInstance()->IsControlToggling(RNCSTR("P")));
			
			SetWorldPosition(world->GetHeadCamera()->GetWorldPosition());
			SetWorldRotation(world->GetHeadCamera()->GetWorldRotation());
			_hand[0]->SetWorldRotation(GetWorldRotation());
			_hand[1]->SetWorldRotation(GetWorldRotation());
			_hand[0]->SetWorldPosition(GetWorldPosition() + RN::Vector3(0.0f, -1.0f, 0.0f) + _hand[0]->GetWorldRotation().GetRotatedVector(RN::Vector3(-0.5, 0.0, -0.2)));
			_hand[1]->SetWorldPosition(GetWorldPosition() + RN::Vector3(0.0f, -1.0f, 0.0f) + _hand[0]->GetWorldRotation().GetRotatedVector(RN::Vector3(0.5, 0.0, -0.2)));
			UpdateBody(delta);
			PlayerGame::Update(delta);
			return;
		}
		
		//Remove reference in case it was removed from the scene
		if(_groundLevelNode && !_groundLevelNode->GetSceneInfo())
		{
			SafeRelease(_groundLevelNode);
			if(_isAirJumping)
			{
				_isAirJumping = false;
				_isOnGround = false;
			}
		}
		
		//Make the player fall if holding with two hands while above an object that doesn't collide
		//This makes them fall if a crumbling level node disappears
		if(_isAirJumping && _groundLevelNode && !_groundLevelNode->CanCollide())
		{
			_isAirJumping = false;
			_isOnGround = false;
			SafeRelease(_groundLevelNode);
		}
		
		_feet->SetPosition(RN::Vector3(0.0f, std::min(-vrCamera->GetHead()->GetPosition().y, 0.0f), 0.0f));
		
		RN::VRControllerTrackingState leftHandController = vrCamera->GetControllerTrackingState(0);
		RN::VRControllerTrackingState rightHandController = vrCamera->GetControllerTrackingState(1);

		RN::Vector3 rawControllerPosition[2];
		rawControllerPosition[0] = leftHandController.positionGrip;
		rawControllerPosition[1] = rightHandController.positionGrip;

		RN::Vector3 rawControllerVelocity[2];
		rawControllerVelocity[0] = leftHandController.velocityLinear;
		rawControllerVelocity[1] = rightHandController.velocityLinear;
		
		RN::Vector3 snapTurnMovement;
		if(World::GetSharedInstance()->GetSettingsManager().GetTurnMode() == SettingsManager::TurnModeSnap)
		{
			//Snap turning
			float turnValue = rightHandController.thumbstick.x;
			if(rightHandController.type == RN::VRControllerTrackingState::Type::HTCViveController && rightHandController.button[RN::VRControllerTrackingState::Button::Pad])
			{
				turnValue = rightHandController.trackpad.x;
			}
			if(std::abs(turnValue) > 0.3f)
			{
				if(_rotateTimer <= RN::k::EpsilonFloat)
				{
					float sign = turnValue > 0.0 ? -1.0 : 1.0;
					if(_activeHand == -1)
					{
						vrCamera->Rotate(RN::Vector3(45.0f * sign, 0.0, 0.0));
					}
					else
					{
						if(_isAirJumping) //Holding on to air with both hands
						{
							snapTurnMovement = GetWorldPosition() - _hand[0]->GetWorldPosition() * 0.5f - _hand[1]->GetWorldPosition() * 0.5f;
						}
						else //Holding on to something with just one hand
						{
							snapTurnMovement = GetWorldPosition() - _hand[_activeHand]->GetWorldPosition();
						}
						snapTurnMovement.y = 0.0f;
						snapTurnMovement = RN::Quaternion(RN::Vector3(45.0f * sign, 0.0f, 0.0f)).GetRotatedVector(snapTurnMovement) - snapTurnMovement;
						vrCamera->Rotate(RN::Vector3(45.0f * sign, 0.0, 0.0));
					}
					
					_rotateTimer = 0.25f;
				}
			}
			else
			{
				_rotateTimer = 0.0f;
			}
			_rotateTimer = std::max(_rotateTimer - delta, 0.0f);
		}
		else if(World::GetSharedInstance()->GetSettingsManager().GetTurnMode() == SettingsManager::TurnModeSmooth)
		{
			//Smooth turning
			float turnValue = rightHandController.thumbstick.x;
			if(rightHandController.type == RN::VRControllerTrackingState::Type::HTCViveController && rightHandController.button[RN::VRControllerTrackingState::Button::Pad])
			{
				turnValue = rightHandController.trackpad.x;
			}
			
			float smoothTurnSpeed = World::GetSharedInstance()->GetSettingsManager().GetSmoothTurnSpeed() * 10.0f;
			if(_activeHand == -1)
			{
				vrCamera->Rotate(RN::Vector3(-turnValue * delta * smoothTurnSpeed, 0.0, 0.0));
			}
			else //Holding on to something with just one hand
			{
				if(_isAirJumping) //Holding on to air with both hands
				{
					snapTurnMovement = GetWorldPosition() - _hand[0]->GetWorldPosition() * 0.5f - _hand[1]->GetWorldPosition() * 0.5f;
				}
				else //Holding on to something with just one hand
				{
					snapTurnMovement = GetWorldPosition() - _hand[_activeHand]->GetWorldPosition();
				}
				snapTurnMovement.y = 0.0f;
				snapTurnMovement = RN::Quaternion(RN::Vector3(-turnValue * delta * smoothTurnSpeed, 0.0f, 0.0f)).GetRotatedVector(snapTurnMovement) - snapTurnMovement;
				vrCamera->Rotate(RN::Vector3(-turnValue * delta * smoothTurnSpeed, 0.0, 0.0));
			}
		}
        else
        {
            //No turning, nothing to do for this case
        }

		leftHandController.rotationAim = vrCamera->GetWorldRotation() * leftHandController.rotationAim;
		leftHandController.positionGrip = vrCamera->GetWorldRotation().GetRotatedVector(leftHandController.positionGrip);
		rightHandController.rotationAim = vrCamera->GetWorldRotation() * rightHandController.rotationAim;
		rightHandController.positionGrip = vrCamera->GetWorldRotation().GetRotatedVector(rightHandController.positionGrip);

		//Movement
		RN::Vector3 localMovement;

		bool isWalkGrab = false;
		bool isActiveHandFixed = false;
		if(_activeHand == -1)
		{
			_twoHandedGrabTimer = 0.0f;
			localMovement = vrCamera->GetHead()->GetPosition() - _previousHeadPosition;
			localMovement = vrCamera->GetWorldRotation().GetRotatedVector(localMovement);
			_speedFromHand = RN::Vector3();
			_speedFromGrabbedObject = RN::Vector3();
		}
		else if(_hand[_activeHand]->GetState() == HandGame::StateGrabbingSolid) //Holding on to something
		{
			_twoHandedGrabTimer = 0.0f;
			RN::Vector3 activeHandDiff = vrCamera->GetHead()->GetPosition() - rawControllerPosition[_activeHand];
			localMovement = activeHandDiff - _lastHandToHeadDiff[_activeHand];
			localMovement = vrCamera->GetWorldRotation().GetRotatedVector(localMovement);
			
			bool isHoldingOtherPlayer = false;
			for(int i = 0; i < 2; i++)
			{
				//Holding on to another player
				RN::SceneNode *grabbedObject = SafeRetain(_hand[i]->GetGrabbedObject());
				RN::SceneNode *grabbedObjectParent = grabbedObject? SafeRetain(grabbedObject->GetParent()) : nullptr;
				if(grabbedObject && grabbedObject->GetSceneInfo() && grabbedObjectParent && grabbedObjectParent->IsKindOfClass(PlayerGameInterpolated::GetMetaClass()) && !static_cast<PlayerGameInterpolated*>(grabbedObjectParent)->GetWantsToRespawn())
				{
					RN::Vector3 localHandPosition = grabbedObject->GetWorldRotation().GetRotatedVector(_hand[i]->GetGrabbedObjectToHandDiff());
					RN::Vector3 newHandPosition = grabbedObject->GetWorldPosition() + localHandPosition;
					
					if(i == _activeHand)
					{
						RN::Vector3 handPositionDiff = newHandPosition - _hand[i]->GetWorldPosition();
						localMovement += handPositionDiff;
						
						_speedFromGrabbedObject = handPositionDiff/delta;
					}
					
					//TODO: This is still somehow overwritten further down... but things break without it too -.-
					_hand[i]->SetWorldPosition(newHandPosition);
					isHoldingOtherPlayer = true;
				}
				if(grabbedObject) grabbedObject->Release();
				if(grabbedObjectParent) grabbedObjectParent->Release();
			}
			
			if(!isHoldingOtherPlayer)
			{
				isActiveHandFixed = true;
			}
			
			_speedFromHand = -vrCamera->GetWorldRotation().GetRotatedVector(rawControllerVelocity[_activeHand]);
			_speed = RN::Vector3();
		}
		else if((_hand[0]->GetState() == HandGame::StateGrabbingAir || _hand[0]->GetState() == HandGame::StateGrabbingEmpty) && (_hand[1]->GetState() == HandGame::StateGrabbingAir || _hand[1]->GetState() == HandGame::StateGrabbingEmpty) && ((_groundCollisionType != Types::CollisionLevelIce && _isOnGround) || _isAirJumping)) //Both hands are grabbing air to jump up
		{
			_twoHandedGrabTimer = 0.0f;
			_speedFromHand = RN::Vector3();
			for(int i = 0; i < 2; i++)
			{
				RN::Vector3 activeHandDiff = vrCamera->GetHead()->GetPosition() - rawControllerPosition[i];
				localMovement += (activeHandDiff - _lastHandToHeadDiff[i]) * 0.5f;
				
				_speedFromHand += -vrCamera->GetWorldRotation().GetRotatedVector(rawControllerVelocity[_activeHand]) * 0.6; //Make jumping with two hands slightly more powerful than one handed if done right (by using 0.6 instead of 0.5 as factor here)
			}
			
			localMovement = vrCamera->GetWorldRotation().GetRotatedVector(localMovement);
			_speed = RN::Vector3();
			
			if(!_isAirJumping)
			{
				_hand[0]->DoGrabVibration();
				_hand[1]->DoGrabVibration();
			}
			_isAirJumping = true;
			_didPlayGetupSound = false;
		}
		else if(_twoHandedGrabTimer <= 0.0f && _isOnGround && (_hand[0]->GetState() == HandGame::StateGrabbingAir || _hand[1]->GetState() == HandGame::StateGrabbingAir || _hand[0]->GetState() == HandGame::StateGrabbingEmpty || _hand[1]->GetState() == HandGame::StateGrabbingEmpty)) //Only one hand is grabbing air to walk around, only works on the ground
		{
			//tracking property will be false if app has no input focus, this prevents the "car glitch"
			if((_activeHand == 0 && leftHandController.tracking) || (_activeHand == 1 && rightHandController.tracking))
			{
				_speedFromHand = -vrCamera->GetWorldRotation().GetRotatedVector(rawControllerVelocity[_activeHand]);
				_speedFromHand.y = 0.0f;
			}
			
			localMovement = vrCamera->GetHead()->GetPosition() - _previousHeadPosition;
			localMovement = vrCamera->GetWorldRotation().GetRotatedVector(localMovement);
			
			if(_groundCollisionType == Types::CollisionLevelIce && _isOnGround)
			{
				_speed += _speedFromHand * delta * 10.0f;
			}
			else
			{
				_speed += _speedFromHand * delta * 20.0f;
			}
			
			_speedFromHand = RN::Vector3();
			isWalkGrab = true;
		}
		else if(_hand[0]->GetState() == HandGame::StateGrabbingAir || _hand[1]->GetState() == HandGame::StateGrabbingAir || _hand[0]->GetState() == HandGame::StateGrabbingEmpty || _hand[1]->GetState() == HandGame::StateGrabbingEmpty)
		{
			_twoHandedGrabTimer -= delta;
			isWalkGrab = true;
		}
		
		//Grapple
		bool isGrappling = false;
		float shortRopeLength = 1000000.0f;
		RN::Vector3 grappleSpeed;
		for(int i = 0; i < 2; i++)
		{
			if(_hand[i]->GetState() == HandGame::StateGrapplingSolid)
			{
				_isOnGround = false;
				_groundCollisionType = 0;
				RN::Vector3 grappleDiff = _hand[i]->GetGrappleDiff() / delta;
				float ropeCorrectionDistance = grappleDiff.GetLength();
				float ropeFactor = grappleDiff.GetNormalized().GetDotProduct(_speed);
				if(ropeFactor < ropeCorrectionDistance && _hand[i]->GetNeedsToLimitForGrappleRope())
				{
					float correctionSpeed = -ropeFactor + std::min(std::min(ropeCorrectionDistance * delta * 5.0f, ropeCorrectionDistance), 10.0f);
					grappleSpeed += grappleDiff.GetNormalized(correctionSpeed);
				}
				
				if(shortRopeLength > _hand[i]->GetGrappleRopeLength()) shortRopeLength = _hand[i]->GetGrappleRopeLength();
				isGrappling = true;
			}
		}
		
		if(isGrappling)
		{
			if(_hand[0]->GetState() == HandGame::StateGrapplingSolid && _hand[1]->GetState() == HandGame::StateGrapplingSolid)
			{
				grappleSpeed *= 0.25f;
			}
			_speed += grappleSpeed;
			
			//Set some dampening for the movement speed depending on the grapple length
			float newDampingFactor = 0.3f - std::min(shortRopeLength/10.0f, 1.0f) * 0.3f;
			if(_dampingFactor < newDampingFactor)
			{
				_dampingFactor += delta * 0.1f;
				if(_dampingFactor > newDampingFactor)
				{
					_dampingFactor = newDampingFactor;
				}
			}
			else
			{
				_dampingFactor -= delta * 0.1f;
				if(_dampingFactor < newDampingFactor)
				{
					_dampingFactor = newDampingFactor;
				}
			}
		}

		_previousHeadPosition = vrCamera->GetHead()->GetPosition();
		_lastHandToHeadDiff[0] = vrCamera->GetHead()->GetPosition() - rawControllerPosition[0];
		_lastHandToHeadDiff[1] = vrCamera->GetHead()->GetPosition() - rawControllerPosition[1];
		
		if(!_isOnGround && (!_activeHand || _hand[_activeHand]->GetState() != HandGame::StateGrabbingSolid))
		{
			if(!isGrappling)
			{
				_dampingFactor -= delta * 0.1f;
				if(_dampingFactor < 0.0f) _dampingFactor = 0.0f;
			}
			
			//Apply a little bit of dampening / air friction to keep the grappling stable, but it also slows down jumping
			_speed -= _speed * _dampingFactor * delta;
		}
		else
		{
			_dampingFactor = 0.0f;
		}

		//Move!
		_controller->Move(_handGrabCorrectionSpeed + snapTurnMovement + localMovement + RN::Vector3(_speed.x, 0.0f, _speed.z) * delta, delta);
		
		//Gravity
		bool wasOnGround = _isOnGround;
		bool wasOnIce = _groundCollisionType == Types::CollisionLevelIce;
		bool wasFeetBounce = _isFeetBounce;
		_isOnGround = false;
		_isFeetBounce = false;
		
		//Make the player stand on their feet and apply gravity if in the air, but not holding on to anything
		RN::PhysXContactInfo contactInfo = _controller->SweepTest(RN::Vector3(0.0f, -100.0, 0.0f));
		
		//In case of hitting a cubes corner with the sweep test above the normal will point in a bad direction pushing the player off, doing a raycast after forces a more useful normal
		if(contactInfo.distance >= 0.0)
		{
			contactInfo = world->GetPhysicsWorld()->CastRay(contactInfo.position + RN::Vector3(0.0f, contactInfo.distance, 0.0f), contactInfo.position - RN::Vector3(0.0f, 1.0f, 0.0f), _controller->GetCollisionFilterMask());
		}
		
		float instantFallHeight = -_feet->GetPosition().y - std::min(_speed.y, 0.0f) * delta;
		if(wasOnGround && contactInfo.distance >= 0.0 && contactInfo.normal.y > RN::k::EpsilonFloat)
		{
			RN::Vector3 slopeVector = contactInfo.normal.GetCrossProduct(RN::Vector3(_speed.x, 0.0f, _speed.z));
			slopeVector = slopeVector.GetCrossProduct(contactInfo.normal);
			slopeVector.Normalize();
			
			if(std::abs(slopeVector.x) > RN::k::EpsilonFloat)
			{
				float slopeCorrectionX = -slopeVector.y * _speed.x * delta / slopeVector.x;
				float slopeCorrectionZ = -slopeVector.y * _speed.z * delta / slopeVector.z;
				float newSlopeCorrection = sqrt(slopeCorrectionX * slopeCorrectionX + slopeCorrectionZ * slopeCorrectionZ);
				
				//Only use this going down
				if(slopeVector.y < 0.0f)
				{
					instantFallHeight += _slopeCorrection + 0.01f; //Add a little extra
					//RNDebug("Slope correction: " << _slopeCorrection << ", instant fall height: " << instantFallHeight);
				}
				_slopeCorrection = newSlopeCorrection;
			}
			else
			{
				instantFallHeight += 0.1f;
			}
		}
		
		if(contactInfo.distance > -0.5f)
		{
			_groundCollisionType = contactInfo.node->GetAttachments()->GetObjectAtIndex<RN::PhysXStaticBody>(0)->GetCollisionFilterGroup();
		}
		else
		{
			_groundCollisionType = 0;
		}
		
		bool tooSteepToBeGround = false;
		if(contactInfo.normal.y < 0.2f)
		{
			//Check where the player feet would touch the ground
			tooSteepToBeGround = true;
			
			RN::Vector3 slopeVector = contactInfo.normal.GetCrossProduct(RN::Vector3(0.0f, 1.0f, 0.0f));
			slopeVector = slopeVector.GetCrossProduct(contactInfo.normal);

			if(!RN::Math::Compare(slopeVector.y, 0.0f))
			{
				RN::Vector3 newFeetPosition = slopeVector / slopeVector.y;
				newFeetPosition *= _feet->GetPosition().y;
				
				//Trace down at this new position to see if it hits ground that the player can stand on
				RN::PhysXContactInfo newContactInfo = world->GetPhysicsWorld()->CastRay(GetWorldPosition(), GetWorldPosition() + newFeetPosition * 2.0f, Types::CollisionLevel);
				if(newContactInfo.distance > -0.5f && newContactInfo.normal.y >= 0.2f)
				{
					contactInfo = newContactInfo;
					
					//Correct for the ray being angled, there is still a tiny offset somehow, but got to be good enough for now
					contactInfo.distance = GetWorldPosition().y - HEAD_COLLIDER_RADIUS - HEAD_COLLIDER_HEIGHT * 0.5f - newContactInfo.position.y;

					tooSteepToBeGround = false;
				}
			}
		}
		
		if(contactInfo.distance > -0.5f && contactInfo.distance <= instantFallHeight && !tooSteepToBeGround)
		{
			//Respawn player if lava was hit.
			if(contactInfo.node->GetAttachments()->GetObjectAtIndex<RN::PhysXStaticBody>(0)->GetCollisionFilterGroup() == Types::CollisionLevelLava || contactInfo.node->GetAttachments()->GetObjectAtIndex<RN::PhysXStaticBody>(0)->GetCollisionFilterGroup() == Types::CollisionLevelGrapplableLava)
			{
				PlayDeathSound(true);
				Respawn();
			}
			
			if(_hand[0]->GetState() != HandGame::StateGrapplingSolid && _hand[1]->GetState() != HandGame::StateGrapplingSolid)
			{
				//Player is on a bounce block
				if(_groundCollisionType == Types::CollisionLevelBouncing)
				{
					if(contactInfo.normal.y > RN::k::EpsilonFloat && (!wasOnGround || wasOnIce) && !_isBlockedAbove && !wasFeetBounce) //checking the contact normal here to only make the feet bounce off something the head can't collide with)
					{
						RN::Vector3 euler = _head->GetWorldRotation().GetEulerAngle();
						euler.x *= -1.0;
						euler.y = 0.0;
						euler.z = 0.0;
						PlayBounceSound(-contactInfo.normal.GetDotProduct(_previousSpeed), RN::Quaternion(euler).GetRotatedVector(contactInfo.position - _controller->GetWorldPosition()).GetNormalized());
						
						_speed = _speed - contactInfo.normal * _speed.GetDotProduct(contactInfo.normal) * 2.0f;
						_speed *= BOUNCE_SPEED_FACTOR;
						if(_speed.GetDotProduct(contactInfo.normal) < 0.2f) //If speed along normal is too small, just start standing on the surface
						{
							_isOnGround = true;
						}
						else
						{
							_isFeetBounce = true;
						}
					}
					else if(_speed.GetDotProduct(contactInfo.normal) < 0.2f) //Only put on ground if still moving towards the block or not bouncing fast enough, this prevents the player from just standing on a bounce block while the head is lower than the player height and the speed pushing the player back keeps them in reach of the block
					{
						_isOnGround = true;
					}
					else
					{
						_isFeetBounce = true; //Player is still doing intial bounce
					}
				}
				else
				{
					//Player is on any other block
					_isOnGround = true;
					
					SafeRelease(_groundLevelNode);
					//Trigger level node action if player is standing on it
					if(contactInfo.node && contactInfo.node->IsKindOfClass(LevelNode::GetMetaClass()))
					{
						LevelNode *levelNode = contactInfo.node->Downcast<LevelNode>();
						levelNode->Trigger();
						_groundLevelNode = SafeRetain(levelNode);
					}
					
					if(!wasOnGround && _previousSpeed.y < -1.0f)
					{
						//RNDebug("Is on ground: " << contactInfo.distance - instantFallHeight);
						PlayLandSound(-_previousSpeed.y);
					}
				}
			}
		}
		else
		{
			if(wasOnGround)
			{
				//RNDebug("Is in air: " << contactInfo.distance - instantFallHeight);
			}
			
			if(contactInfo.distance - instantFallHeight > 0.1f || contactInfo.distance < -0.5f)
			{
				PlaySlideSound(0.0f); //Stop ice sound if not on the ground
			}
			_didPlayGetupSound = false;
		}
		
		_previousSpeed = _speed;
		
		//A tangent of the surface the player is standing on
		RN::Vector3 slopeVector = contactInfo.normal.GetCrossProduct(RN::Vector3(0.0f, 1.0f, 0.0f));
		slopeVector = slopeVector.GetCrossProduct(contactInfo.normal);
		slopeVector.Normalize();
		
		_isSliding = false;
		
		if(_rampJumpTimer > 0.0f)
		{
			_rampJumpTimer -= delta;
		}
		
		if(_isOnGround)
		{
			//standing on a sloped surface will make the player slide downwards
			//Only slide on ice or if the angle is too steep
			if(_groundCollisionType == Types::CollisionLevelIce || slopeVector.y > 0.5)
			{
				_isSliding = true;
				float sign = (slopeVector.y > 0.0f)? -1.0f : 1.0f; //Sign is probably not needed, but maybe it is... y is supposed to always by negative (or 0)
				RN::Vector3 slideAcceleration = slopeVector * slopeVector.y * 9.81f * 3.0f * sign;
				_speed += slideAcceleration * delta;
			}
			
			//Apply friction if not sliding
			if(!_isSliding)
			{
				PlaySlideSound(0.0f); //Stop ice sound if not sliding
				
				RN::Vector2 horizontalSpeed = RN::Vector2(_speed.x, _speed.z);
				float currentSpeed = horizontalSpeed.GetLength();
				
				float speedChange = currentSpeed * 5.0 * delta / (1.0f + 0.15f * currentSpeed);
				if(std::abs(speedChange) > std::abs(currentSpeed))
				{
					speedChange = currentSpeed;
				}
				horizontalSpeed.Normalize(std::min(currentSpeed - speedChange, MAX_WALK_SPEED));
				_speed.x = horizontalSpeed.x;
				_speed.z = horizontalSpeed.y;
				
				_playerWalkDistanceForNextStepSound += horizontalSpeed.GetLength() * delta;
				if(_playerWalkDistanceForNextStepSound > 2.0f)
				{
					_playerWalkDistanceForNextStepSound = 0.0f;
					PlayStepSound(_previousSpeed.GetLength());
				}
			}
			else
			{
				PlaySlideSound(_previousSpeed.GetLength());
			}
			
			//Only start ramp timer if the floor isn't horizontal and the normal actually changed
			if(contactInfo.normal.y < 0.99f && (std::abs(contactInfo.normal.x - _slidingUpNormal.x) > 0.01f || std::abs(contactInfo.normal.y - _slidingUpNormal.y) > 0.01f || std::abs(contactInfo.normal.z - _slidingUpNormal.z) > 0.01f))
			{
				bool wasSlidingUp = _isSlidingUp;
				_isSlidingUp = _speed.GetDotProduct(slopeVector) > 0.0f && contactInfo.normal.y < 0.99;
				if(wasSlidingUp && !_isSlidingUp)
				{
					//RNDebug("RAMP!");
					_isJumpingUp = true;
					_rampJumpTimer = 0.1f;
				}
			}
		}
		_slidingUpNormal = contactInfo.normal;
		
		if(_activeHand == -1 || ((_hand[_activeHand]->GetState() == HandGame::StateGrabbingAir || _hand[_activeHand]->GetState() == HandGame::StateGrabbingEmpty) && !_isAirJumping)) //One handed air grabs for movement still require gravity
		{
			float backToGroundMovementDist = 0.0f;
			if(!_isOnGround || _rampJumpTimer > 0.0f)
			{
				_speed.y -= 9.81*delta;
				if(_speed.y < 0.0f) _isJumpingUp = false;
				_didPlayGetupSound = false;
				//RNDebug("Gravity");
			}
			else
			{
				float distanceToMove = ((-_feet->GetPosition().y) - contactInfo.distance);
				if(distanceToMove < 0)
				{
					//Prevent stopping the player when throwing up while the feet are touching a surface
					if(!_isJumpingUp)
					{
						//This will keep the player on the floor
						_speed.y = distanceToMove / delta;
						_didPlayGetupSound = false;
					}
				}
				else
				{
					//Standup slower if the surface below player is at a steep angle
					float normalFactor = 2.0f * std::acos(contactInfo.normal.y);
					normalFactor /= RN::k::Pi;
					normalFactor = 1.0f - normalFactor;
					float standUpSpeedFactor = normalFactor * normalFactor * normalFactor * 6.0f;
					
					//Standup faster if the player is going fast
					standUpSpeedFactor *= std::max(std::min(sqrt((_speed.x * _speed.x + _speed.z * _speed.z))/10.0f, 10.0f), 1.0f);
					
					float standUpSpeed = distanceToMove * standUpSpeedFactor;
					if(!_isJumpingUp || standUpSpeed > _speed.y)
					{
						//Slowly stand up if inside the floor
						_speed.y = standUpSpeed;
						if(_speed.y * delta >= distanceToMove)
						{
							_speed.y = 0.0f;
							backToGroundMovementDist = distanceToMove;
						}
						_isJumpingUp = false;
						
						if(distanceToMove > 0.2f && !_didPlayGetupSound)
						{
							PlayLandSound(distanceToMove);
							_didPlayGetupSound = true;
						}
					}
				}
			}
			
			//Apply gravity
			_controller->Move(RN::Vector3(0.0f, _speed.y * delta + backToGroundMovementDist, 0.0f), delta);
		}
		
		//Update Attachments and stuff
		PlayerGame::Update(delta);

		//Update camera position for local movement
		RN::Vector3 cameraUpdateDiff = vrCamera->GetWorldPosition() - vrCamera->GetHead()->GetWorldPosition();
		vrCamera->SetWorldPosition(cameraUpdateDiff + GetWorldPosition());

		//Hand placement
		RN::Vector3 controllerPosition[2];
		controllerPosition[0] = vrCamera->GetWorldPosition() - GetWorldPosition() + leftHandController.positionGrip;
		controllerPosition[1] = vrCamera->GetWorldPosition() - GetWorldPosition() + rightHandController.positionGrip;
		
		_hand[0]->SetPosition(controllerPosition[0]);
		_hand[0]->SetRotation(leftHandController.rotationAim);

		_hand[1]->SetPosition(controllerPosition[1]);
		_hand[1]->SetRotation(rightHandController.rotationAim);
		
		//Body rotation
		UpdateBody(delta);

		bool wasGrappling = (_hand[0]->GetIsGrappling() || _hand[1]->GetIsGrappling());
		for(int i = 0; i < 2; i++)
		{
			RN::VRControllerTrackingState controller = (i == 0)?leftHandController:rightHandController;
			if(controller.type == RN::VRControllerTrackingState::Type::ValveIndexController)
			{
				controller.handTrigger = controller.handTrigger * 0.5f + 0.5f;
			}
			float lettingGoValue;
			lettingGoValue = controller.handTrigger - _lastHandTriggerValue[i];
			_lastHandTriggerValue[i] = controller.handTrigger;

			_hand[i]->SetIsGrapplePulling(controller.indexTrigger > 0.98f);
			_hand[i]->UpdateOverlap(_speed, delta);
			
			bool startGrabbing = (controller.handTrigger > 0.1f && lettingGoValue > RN::k::EpsilonFloat);
			
			//Handle actual grabbing
			if(_hand[i]->GetState() == HandGame::StateNone)
			{
				if(startGrabbing)
				{
					if(!_didHandLetGo[i])
					{
						_hand[i]->Grab(true, _isOnGround);
						
						if(_hand[i]->GetState() == HandGame::StateGrabbingAir || _hand[i]->GetState() == HandGame::StateGrabbingEmpty)
						{
							_twoHandedGrabTimer = 0.1;
						}
					}
				}
				else
				{
					_didHandLetGo[i] = false;
				}
			}
			else
			{
				if(controller.type == RN::VRControllerTrackingState::Type::ValveIndexController)
				{
					if(controller.handTrigger < 0.7f && lettingGoValue < -RN::k::EpsilonFloat)
					{
						_hand[i]->Grab(false, false);
						_didHandLetGo[i] = true;
					}
				}
				else if(controller.handTrigger < 0.9f && lettingGoValue < -RN::k::EpsilonFloat)
				{
					_hand[i]->Grab(false, false);
					_didHandLetGo[i] = true;
				}
			}

			bool startGrappling = (!World::GetSharedInstance()->GetInputManager()->GetHasInputFocus() && controller.indexTrigger > 0.1f);
			
			if(startGrappling && _hand[i]->GetState() == HandGame::StateNone && !_wasTriggerPressed[i])
			{
				_hand[i]->Grapple(true);
			}
			if(!startGrappling && _hand[i]->GetIsGrappling())
			{
				_hand[i]->Grapple(false);
			}
			
			_wasTriggerPressed[i] = (controller.indexTrigger > 0.1f);
		}
		
		//jumping while grabbing air with both hands needs some special handling when letting go.
		if(_isAirJumping && (_hand[0]->GetState() == HandGame::StateNone || _hand[1]->GetState() == HandGame::StateNone))
		{
			_speed = _speedFromHand.GetNormalized(std::min(_speedFromHand.GetLength(), MAX_SPEED_PUSHING));
			if(_speed.y > 0.0f) _isJumpingUp = true;
			_hand[0]->Grab(false, false);
			_hand[1]->Grab(false, false);
			_didHandLetGo[0] = true;
			_didHandLetGo[1] = true;
			_isAirJumping = false;
			
			//RNDebug("Force let go of airjump grab because one hand did let go");
		}
		
		//TODO: Update the active hand if one of the hands state changed
		for(int i = 0; i < 2; i++)
		{
			if(_hand[i]->GetDidChangeState() && !_hand[i]->GetIsGrappling())
			{
				//Active hand is always the last hand that grabbed, unless the new hand is grabbing air while already holding on to something with the previous one
				if(_activeHand == -1 || _hand[i]->GetState() == HandGame::StateGrabbingSolid || _hand[_activeHand]->GetState() == HandGame::StateGrabbingAir || _hand[_activeHand]->GetState() == HandGame::StateGrabbingEmpty)
				{
					_activeHand = i;
				}
			}
		}

		//Update active hand if player let go of one or both hands
		if(_activeHand != -1 && (_hand[_activeHand]->GetState() == HandGame::StateNone || _hand[_activeHand]->GetIsGrappling()))
		{
			int activeHand = -1;
			for(int hand = 0; hand < 2; hand++)
			{
				if(_hand[hand]->GetState() != HandGame::StateNone && !_hand[hand]->GetIsGrappling())
				{
					activeHand = hand;
				}
			}
			_activeHand = activeHand;

			//Add momentum if letting go, in this case the player will always have been at a full stop so setting it directly is fine, except when stopping to grapple
			if((_activeHand == -1 || _hand[_activeHand]->GetState() == HandGame::StateNone || _hand[_activeHand]->GetState() == HandGame::StateGrabbingEmpty) && !isWalkGrab && !wasGrappling)
			{
				//RNDebug("Player: Adding momentum");
				_speed = _speedFromHand.GetNormalized(std::min(_speedFromHand.GetLength(), MAX_SPEED_PUSHING)) + _speedFromGrabbedObject.GetNormalized(std::min(_speedFromGrabbedObject.GetLength(), MAX_SPEED_FROM_OTHER_PLAYER));
				if(_speed.y > 0.0f) _isJumpingUp = true;
			}
		}
		
		if(_activeHand != -1 && isActiveHandFixed)
		{
			//This keeps a grabbing hand in position to prevent cheating by holding on with both hands and letting go while the hand is in the air but still holding
			RN::Vector3 handPositionDiff = _hand[_activeHand]->GetGrabPosition() - _hand[_activeHand]->GetWorldPosition();
			_handGrabCorrectionSpeed = handPositionDiff.Normalize(std::min(handPositionDiff.GetLength() * 10.0f * delta, handPositionDiff.GetLength()));
		}
		else
		{
			_handGrabCorrectionSpeed = RN::Vector3();
		}
		
		float currentTime = world->GetCurrentServerTime();
		
		PlayerSettings *playerSettings = world->GetPlayerSettings(world->GetClientID());
		if(playerSettings)
		{
			float currentLevelTime = currentTime - playerSettings->GetStartTime();
			_hand[0]->SetWatchData(currentLevelTime, _speed.GetLength());
			
			//Player reached end of the level, change status and inform the server
			RN::Vector3 finishPosition = world->GetLevelManager().GetFinishPosition();
			RN::Vector3 headPosition = GetWorldPosition();
			if(playerSettings->GetIsPlayingLevel() && RN::Vector3(finishPosition.x, 0.0f, finishPosition.z).GetDistance(RN::Vector3(headPosition.x, 0.0f, headPosition.z)) <= world->GetLevelManager().GetFinishRadius() && (headPosition.y - finishPosition.y) < ((-_feet->GetPosition().y)+0.5f) && headPosition.y > finishPosition.y && !_wantsRespawn)
			{
				bool didAlreadyFinishLevel = playerSettings->GetHasFinishedLevel();
				playerSettings->SetIsPlayingLevel(false);
				playerSettings->SetHasFinishedLevel(true);
				
				if(playerSettings->GetBestTime() < RN::k::EpsilonFloat || playerSettings->GetBestTime() > currentLevelTime)
				{
					playerSettings->SetBestTime(currentLevelTime);
					
					//Only for community levels!
					if(world->GetServerSettings().level == World::ServerLevelGame && world->GetServerSettings().status == World::ServerStatusPlaying && world->GetLevelName() && world->GetLevelName()->HasPrefix(RNCSTR("community:")) && !world->GetUserInfoManager().GetIsBanned())
					{
						PlayedLevelRequest::StartWithCallback(LevelManager::GetLevelIDFromDataID(world->GetServerSettings().GetLevelName()), true, currentLevelTime, nullptr);
						
						if(!didAlreadyFinishLevel)
						{
							PauseMenuNode *pauseMenu = world->OpenPauseMenu(false);
							pauseMenu->TransitionToRateLevelView();
						}
					}
				}
				
				PlayLevelFinishedSound();
				
				world->SendPlayerSettings();
			}
		}
		
		if(leftHandController.button[RN::VRControllerTrackingState::Button::Stick] && rightHandController.button[RN::VRControllerTrackingState::Button::Stick])
		{
			if(!_isCheckpointButtonPressed)
			{
				_isCheckpointButtonPressed = true;
				SetCheckpoint();
			}
		}
		else
		{
			_isCheckpointButtonPressed = false;
		}
		
		if(leftHandController.button[RN::VRControllerTrackingState::Button::BY] && rightHandController.button[RN::VRControllerTrackingState::Button::BY])
		{
			if(!_isRespawnButtonPressed)
			{
				_isRespawnButtonPressed = true;
				Respawn();
			}
		}
		else if(!(world->GetServerSettings().level == World::ServerLevelEditor && world->GetServerSettings().status == World::ServerStatusPlaying))
		{
			_isRespawnButtonPressed = false;
		}
		
		//Switch back to edit mode (only in the editor and not testing)
		if(world->GetServerSettings().level == World::ServerLevelEditor && world->GetServerSettings().status == World::ServerStatusPlaying)
		{
			bool isTestButtonPressed = leftHandController.button[RN::VRControllerTrackingState::BY];
			if (leftHandController.type == RN::VRControllerTrackingState::Type::HTCViveController)
			{
				isTestButtonPressed = leftHandController.button[RN::VRControllerTrackingState::Button::Pad] && leftHandController.trackpad.y > 0.0f;
			}
			
			if(isTestButtonPressed)
			{
				_isBackToEditingPressed = true;
			}
			else
			{
				//Switch to edit mode when letting go of the button
				if(_isBackToEditingPressed && !_isRespawnButtonPressed)
				{
					world->RequestEditorPlayerChange(true, GetWorldPosition(), vrCamera->GetWorldRotation());
				}
				_isBackToEditingPressed = false;
				_isRespawnButtonPressed = false; //If in editor, only reset respawning after letting go of testing button
			}
		}
		
		if(playerSettings)
		{
			playerSettings->SetIsPushToTalkButtonPressed(leftHandController.button[RN::VRControllerTrackingState::Button::AX]);
		}
		
		//Respawn the player if outside the level
		if(GetWorldPosition().y < world->GetDeathFallYPosition())
		{
			PlayDeathSound(false);
			Respawn();
		}

		if(_wantsRespawn)
		{
			if(world->GetServerLevel() == World::ServerLevelEditor && world->GetServerSettings().status == World::ServerStatusPlaying)
			{
				Teleport(_spawnPosition);
			}
			else
			{
				//Prevent respawning above things if the player is tall and the checkpoint below something
				RN::PhysXContactInfo contactInfo = world->GetPhysicsWorld()->CastRay(_spawnPosition + RN::Vector3(0.0f, 0.01f, 0.0f), _spawnPosition - _feet->GetPosition(), _controller->GetCollisionFilterMask());
				if(contactInfo.distance < -0.5f) //Nothing is blocking
				{
					contactInfo.position = _spawnPosition - _feet->GetPosition();
				}
				else
				{
					float offset = 0.1f;
					while(contactInfo.distance < 0.01f && offset < 1.0f && offset < -_feet->GetPosition().y) //spawn position is likely inside something, keep trying a little higher
					{
						//Assume that there is nothing blocking 1m higher
						contactInfo = world->GetPhysicsWorld()->CastRay(_spawnPosition + RN::Vector3(0.0f, offset, 0.0f), _spawnPosition - _feet->GetPosition(), _controller->GetCollisionFilterMask());
						offset += 0.1f;
					}
					
					if(contactInfo.distance < 0.01f) //Nothing is blocking or still inside something, so just spawn as intended
					{
						contactInfo.position = _spawnPosition - _feet->GetPosition();
					}
					else
					{
						//Otherwise use a position slightly below the contact point
						contactInfo.position -= RN::Vector3(0.0f, std::min(0.1f, contactInfo.distance), 0.0f);
					}
				}
				Teleport(contactInfo.position);
			}
			
			//Reset the startTime if player isn't respawning to a checkpoint.
			if(playerSettings && playerSettings->GetCheckpointCount() == 0)
			{
				playerSettings->SetStartTime(world->GetCurrentServerTime());
				world->SendPlayerSettings();
			}
			
			_respawnCounter += 1; //Used to let other players know about the respawning to push them off
			_wantsRespawn = false;
			_speed = RN::Vector3();
			_isOnGround = false;
			_groundCollisionType = 0;
			
			_hand[0]->Grab(false, false);
			_hand[1]->Grab(false, false);
			_hand[0]->SetFailedGrappling();
			_hand[1]->SetFailedGrappling();
			_didHandLetGo[0] = true;
			_didHandLetGo[1] = true;
			_activeHand = -1;
		}
		
		//Gets set in the physics collision event, just reset here every frame
		_isBlockedAbove = false;
		
//		vrCamera->GetHead()->SetWorldPosition(RN::Vector3(-18.485, 1.83291, 5.86131));
//		vrCamera->GetHead()->SetWorldRotation(RN::Quaternion(-0.0461506, -0.266848, -0.0127943, 0.962548));
	}

	void PlayerGameInteractive::Teleport(const RN::Vector3 &position)
	{
		PlayerGame::Teleport(position);
		_head->SetPosition(RN::Vector3());
	}

	bool PlayerGameInteractive::SetCheckpoint()
	{
		World *world = World::GetSharedInstance();
		if(world->GetServerLevel() == World::ServerLevelEditor && world->GetServerSettings().status != World::ServerStatusTesting)
		{
			//If playing while in the editor, don't increase the checkpoint counter and no need to set the rotation
			PlayerSettings *playerSettings = world->GetPlayerSettings(world->GetClientID());
			if(!playerSettings) return false;
			
			playerSettings->SetCheckpointPosition(GetWorldPosition());
			return true;
		}
		
		if(_isOnGround && _groundCollisionType != Types::CollisionLevelIce && _groundCollisionType != Types::CollisionLevelBouncing && _groundCollisionType != Types::CollisionLevelGrabbableCrumbling && !_isAirJumping && !_isSliding)
		{
			PlayerSettings *playerSettings = world->GetPlayerSettings(world->GetClientID());
			if(playerSettings && playerSettings->GetCheckpointCount() < world->GetServerSettings().maxCheckpointCount)
			{
				//Trace down to always put the checkpoint on the floor, even if the feet are below the floor
				RN::PhysXContactInfo contactInfo = _controller->SweepTest(_feet->GetPosition());
				if(contactInfo.distance < -0.5f)
				{
					contactInfo.position = GetWorldPosition() + _feet->GetPosition();
				}
				else
				{
					contactInfo.position.y += 0.1f; //Checkpoints are currently all placed 10cm below the origin to make up for the feet being 10cm above the ground and have to be moved up according as the contact position is exactly on the ground
				}
				
				playerSettings->SetCheckpointCount(playerSettings->GetCheckpointCount() + 1);
				playerSettings->SetCheckpointPosition(contactInfo.position);
				RN::Vector3 checkpointRotation = _head->GetWorldRotation().GetEulerAngle();
				checkpointRotation.y = 0.0f;
				checkpointRotation.z = 0.0f;
				playerSettings->SetCheckpointRotation(checkpointRotation);
				world->SendPlayerSettings();
				
				return true;
			}
		}
		
		return false;
	}

	void PlayerGameInteractive::PushOff(int hand)
	{
		if(_hand[hand]->GetState() == HandGame::StateGrabbingSolid)
		{
			RNDebug("got pushed off");
			_didHandLetGo[hand] = true;
			_hand[hand]->SetState(HandGame::StateGrabbingPushed, _hand[hand]->GetStateChangeCounter() + 1);
		}
	}

	Networking::Packet PlayerGameInteractive::CreatePacket() const
	{
		Networking::Packet packet = PlayerGame::CreatePacket();
		return packet;
	}

	Networking::Packet PlayerGameInteractive::ProcessPacket(const Networking::Packet &packet)
	{
		Networking::Packet updatedPacket = PlayerGame::ProcessPacket(packet);
		
		if(updatedPacket.content_case() != Networking::Packet::kSceneNodeUpdate) return updatedPacket;
		if(updatedPacket.scenenodeupdate().content_case() != Networking::SceneNodeUpdate::kPlayerGame) return updatedPacket;
		
		Networking::PlayerGameNode *playerGame = updatedPacket.mutable_scenenodeupdate()->mutable_playergame();
		
		//Handle grabbing on client side
		for(int i = 0; i < 2; i++)
		{
			Networking::HandGame handData = (i == 0)?playerGame->lefthand():playerGame->righthand();
			if(_hand[i]->GetStateChangeCounter() <= handData.statechangecounter())
			{
				if(handData.state() == Networking::HandGame::State::HandGame_State_GRABBING_PUSHED)
				{
					PushOff(i);
				}
			}
		}
		
		return updatedPacket;
	}
}
