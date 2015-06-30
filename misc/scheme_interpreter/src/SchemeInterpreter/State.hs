{-# LANGUAGE TupleSections #-}

{-
 - An implementation of mutable state for Scheme programs.
 -}

module SchemeInterpreter.State where

import qualified SchemeInterpreter.Error as Error
import qualified SchemeInterpreter.Types as Types
import qualified Data.IORef as IORef
import qualified Control.Monad.Error as MonadError
import qualified Control.Monad as Monad

type Env = IORef.IORef [(String, IORef.IORef Types.LispVal)]
type IOThrowsError = MonadError.ErrorT Error.LispError IO

nullEnv :: IO Env
nullEnv = IORef.newIORef []

liftThrows :: Error.ThrowsError a -> IOThrowsError a
liftThrows (Left err) = Error.throwError err
liftThrows (Right val) = return val

runIOThrows :: IOThrowsError String -> IO String
runIOThrows action = fmap (either show id) $ MonadError.runErrorT action

isBound :: Env -> String -> IO Bool
isBound env varName = fmap (maybe False (const True) . lookup varName) $
	IORef.readIORef env

getVar :: Env -> String -> IOThrowsError Types.LispVal
getVar env varName = do
	envVars <- MonadError.liftIO $ IORef.readIORef env
	maybe
		(Error.throwError $
			Error.UnboundVar "Getting an unbound variable" varName)
		(MonadError.liftIO . IORef.readIORef)
		(lookup varName envVars)

setVar :: Env -> String -> Types.LispVal -> IOThrowsError Types.LispVal
setVar env varName value = do
	envVars <- MonadError.liftIO $ IORef.readIORef env
	maybe
		(Error.throwError $
			Error.UnboundVar "Setting an unbound variable" varName)
		(MonadError.liftIO . (flip IORef.writeIORef value))
		(lookup varName envVars)
	return value

defineVar :: Env -> String -> Types.LispVal -> IOThrowsError Types.LispVal
defineVar envRef varName value = do
	alreadyDefined <- MonadError.liftIO $ isBound envRef varName
	if alreadyDefined
		then setVar envRef varName value
		else MonadError.liftIO $ do
			valueRef <- IORef.newIORef value
			envVars <- IORef.readIORef envRef
			IORef.writeIORef envRef ((varName, valueRef) : envVars)
			return value

bindVars :: Env -> [(String, Types.LispVal)] -> IO Env
bindVars envRef varDefs = IORef.readIORef envRef >>= extendEnv >>=
	IORef.newIORef
	where
		extendEnv env = Monad.liftM (++ env) $ mapM addBinding varDefs
		addBinding (varName, value) = fmap (varName, ) $ IORef.newIORef value
