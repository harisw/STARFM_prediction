import time
import progressbar as pb

bar = pb.ProgressBar(max_value=pb.UnknownLength)
for i in range(20):
	time.sleep(0.1)
	bar.update(i)