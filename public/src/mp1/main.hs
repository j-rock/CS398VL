module Main where

import System.Environment (getArgs)
import Data.Char (isAlpha, toLower)
import Data.List (stripPrefix)


alphas = filter isAlpha
lowerize = map toLower
smartWords = words . map spacify
  where
    spacify x = if bad x then ' ' else x
    bad x = not $ isAlpha x || (== '\'') x

dropPoss x = maybe x id (fmap reverse $ tryStrip x)
  where
    tryStrip = stripPrefix "s'" . reverse

main = do
  [file] <- getArgs
  text <- readFile file
  putStrLn $ unwords . map (lowerize . alphas) . map dropPoss . smartWords $ text
