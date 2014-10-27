##
#	\namespace	blur3d.api.abstract.abstractsceneanimationcontroller
#
#	\remarks	The AbstractSceneAnimationController class defines a base class for managing animation curves within a 3d scene
#
#	\author		eric@blur.com
#	\author		Blur Studio
#	\date		03/15/10
#

from blur3d import abstractmethod
from blur3d.api import SceneWrapper
from blur3d import api


class AbstractSceneAnimationController(SceneWrapper):
	#--------------------------------------------------------------------------------
	#								private methods
	#--------------------------------------------------------------------------------

	@abstractmethod
	def _createNativeKeyAt(self, time):
		"""Creates a new key at the inputed time
		
		:type time: float
		:return: nativeKey or None

		"""
		return None

	@abstractmethod
	def _nativeKeys(self):
		"""Return a list of the keys that are defined for this controller
		
		:return: a list of nativeKeys
		
		"""
		return []

	@abstractmethod
	def _setNativeKeyAt(self, time, nativeKey):
		"""
			\remarks	set the key at the inputed time to the given native key
			\param		time		<float>
			\param		nativeKey	<variant>
			\return		<bool> success
		"""
		return False

	@classmethod
	def _createNewNative(cls, scene, controllerType):
		"""
			\remarks	create a new native controller in the scene of the inputed controller type
			\param		scene				<blur3d.api.Scene>
			\param		controllerType		<blur3d.constants.ControllerType>
			\return		<blur3d.api.SceneAnimationController> || None
		"""
		return None

	#--------------------------------------------------------------------------------
	#								public methods
	#--------------------------------------------------------------------------------
	def createKeyAt(self, time):
		"""Creates a new key at the inputed time
		
		:param time: time to create a key at.
		:type time: float
		:return: the new animation key
		:rtype: :class:`blur3d.api.SceneAnimationKey` or None

		"""
		nativeKey = self._createNativeKeyAt(time)
		if (nativeKey):
			from blur3d.api import SceneAnimationKey
			return SceneAnimationKey(self._scene, nativeKey)
		return None

	@abstractmethod
	def controllerType(self):
		"""Return the type of controller that this controller is
		
		:return: :data:`blur3d.constants.ControllerType`
		
		"""
		return 0

	def isKeyedAt(self, time):
		"""Return whether or not a key exists at the inputed time frame
		
		:param time: time to check key at
		:type time: float
		:return: True if keyed
		:rtype: bool

		"""
		return self.keyAt(time) != None

	def keyAt(self, time):
		"""Return the key that is found at the inputed time frame
		
		:param time: time to get key at.
		:type time: float
		:return: the animation key
		:rtype: :class:`blur3d.api.SceneAnimationKey` or None	

		"""
		for key in self.keys():
			if (key.time() == time):
				return key
		return None

	def keys(self):
		"""
		Return a list of:class: `blur3d.api.SceneAnimationKey`'s that are 
		defined for this controller
		
		:return: a list of :class:`blur3d.api.SceneAnimationKey`'s
		
		"""
		from blur3d.api import SceneAnimationKey
		return [ SceneAnimationKey(self._scene, nativeKey) for nativeKey in self._nativeKeys() ]

	@abstractmethod
 	def valueAtFrame(self, frame):
 		return 0.0
 		
 	@abstractmethod
 	def framesForValue(self, value):
 		return []

 	@abstractmethod
 	def fromAlembic(self, alembic):
 		""" Loads data from an alembic curve file.
 		"""
 		return False

	def removeKeyAt(self, time):
		"""Clears the key at the inputed time
		
		:param time: time to check key at
		:type time: float
		:return: True if key was removed
		:rtype: bool
		
		"""
		return self.setKeyAt(time, None)

	def setKeyAt(self, time, key):
		"""Set the key at the inputed time frame to the inputed key

		:param time: time to set key at.
		:type time: float
		:param key: the animation key
		:type key: :class:`blur3d.api.SceneAnimationKey`
		:return: the animation key
		:rtype: :class:`blur3d.api.SceneAnimationKey` or None	

		"""
		nativeKey = None
		if (key):
			nativeKey = key.nativePointer()
		return self._setNativeKeyAt(time, nativeKey)

	@abstractmethod
  	def toAlembic(self, path=''):
 		""" Returns a alembic curve.

 		Args:
 			path(boolean): Save the curve to disk if provided.
 		"""
 		return False

	@classmethod
	def createNew(cls, scene, controllerType):
		"""Create a new controller in the scene of the inputed controller type
		
		:param scene: :class:`blur3d.api.Scene`
		:param controllerType: :data:`blur3d.constants.ControllerType`
		:return: the new :class:`blur3d.api.SceneAnimationController` or None
		
		"""
		nativeController = cls._createNewNative(scene, controllerType)
		if (nativeController):
			from blur3d.api import SceneAnimationController
			return SceneAnimationController(scene, nativeController)
		return None


# register the symbol
api.registerSymbol('SceneAnimationController', AbstractSceneAnimationController, ifNotFound=True)
