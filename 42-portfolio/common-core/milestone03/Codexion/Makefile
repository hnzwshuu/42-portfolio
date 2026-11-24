NAME := codexion
CC := cc
CFLAGS := -Wall -Wextra -Werror -pthread
CPPFLAGS := -Iinclude
OBJ_DIR := build
SOURCES := src/acquire.c \
	src/clock.c \
	src/coder.c \
	src/coder_thread.c \
	src/config.c \
	src/destroy.c \
	src/diagnostic.c \
	src/error.c \
	src/heap.c \
	src/heap_ops.c \
	src/heap_validate.c \
	src/init.c \
	src/join.c \
	src/launch.c \
	src/log_guard.c \
	src/logging.c \
	src/main.c \
	src/monitor.c \
	src/output.c \
	src/pair_lock.c \
	src/pair_validate.c \
	src/parse.c \
	src/queue.c \
	src/release.c \
	src/report.c \
	src/startup.c \
	src/state.c \
	src/time.c \
	src/validate.c
OBJECTS := $(patsubst src/%.c,$(OBJ_DIR)/%.o,$(SOURCES))
DEPS := $(OBJECTS:.o=.d)

all: $(NAME)

$(NAME): $(OBJECTS)
	$(CC) $(CFLAGS) $(OBJECTS) -o $@

$(OBJ_DIR)/%.o: src/%.c | $(OBJ_DIR)
	$(CC) $(CPPFLAGS) $(CFLAGS) -MMD -MP -c $< -o $@

$(OBJ_DIR):
	mkdir -p $@

clean:
	rm -rf $(OBJ_DIR)

fclean: clean
	rm -f $(NAME)

re: fclean
	$(MAKE) all

-include $(DEPS)

.PHONY: all clean fclean re
