BIN_DIR = bin
EXECUTABLE_PATH = $(BIN_DIR)/rsa

all: $(BIN_DIR) $(EXECUTABLE_PATH)

run: all
	$(EXECUTABLE_PATH)

# `ghc` builds its own dependency tree and only recompiles when it detects
# changes, so we simply force this recipe to run whenever `make` is invoked and
# delegate all of the build logic to `ghc`.
FORCE:
$(EXECUTABLE_PATH): FORCE
	ghc -Wall -fno-warn-type-defaults -O2 \
		-hidir $(BIN_DIR) -odir $(BIN_DIR)\
		-o $@ --make Test.hs \
		../../modular_exponentiation/ModularExponentiation.hs \
		../../extended_euclidean_algorithm/ExtendedEuclideanAlgorithm.hs \
		../../rabin_miller/RabinMiller.hs

$(BIN_DIR):
	mkdir $(BIN_DIR)

clean:
	if [ -d $(BIN_DIR) ]; then rm -rf $(BIN_DIR); fi
