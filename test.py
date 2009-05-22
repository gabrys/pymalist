
from pymalist import play
from fetchers import StdInFetcher
from processors import DummyProcessor
from distributors import TestDistributor
from reactors import StdErrLogger

play(StdInFetcher(), DummyProcessor(), TestDistributor(), StdErrLogger())
