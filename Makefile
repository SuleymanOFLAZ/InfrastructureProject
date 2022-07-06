
COMPILER = gcc
COMPILER_FLAGS = -Wall -O0
INCLUDE_DIR = ./src/include
CODE_DIR = ./src/code
BUILD_DIR = ./build
SRC_FILES = main.c func.c measure.c
OBJ_FILES = main.o func.o measure.o
OBJS = $(patsubst $(CODE_DIR)/%.c, $(BUILD_DIR)/%.o, $(wildcard $(CODE_DIR)/*.c))


all:$(BUILD_DIR)/run.elf

$(BUILD_DIR)/run.elf:$(OBJS)
	$(COMPILER) $(COMPILER_FLAGS) -g -o $@ $(OBJS)

$(BUILD_DIR)/%.o: $(CODE_DIR)/%.c
	$(COMPILER) $(COMPILER_FLAGS) -c -o $@ $< -I$(INCLUDE_DIR)

clean:
	rm -f $(BUILD_DIR)/*.elf $(OBJS)
