TARGET=mainAlphaTwoHB001

OBJE= IOParams.o Gas.o HeatBath.o

OBJS= $(TARGET).o $(OBJE)

LIBS= -lgsl -lgslcblas -lm -lboost_program_options

%.o : %.c
	$(COMPILE) -c $< -o $@ -g -pg

all: $(TARGET)

$(TARGET): $(OBJS)
	$(CXX) -g -o $(TARGET) $(OBJS) $(LIBS) -pg

clean:
	rm -f $(OBJS) $(TARGET)


