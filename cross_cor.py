import numpy as np
from scipy import stats
from scikits.audiolab import wavread
import matplotlib.pyplot as plt
import sys

filename = sys.argv[1]

#data, fs, encoding = wavread('HD Radio split mode audio 5.wav')
data, fs, encoding = wavread(filename)
#data, fs, encoding = wavread('john.wav')
print fs
print data.shape

min_sgmt_seconds = 1

sgmt = fs * min_sgmt_seconds

left, right = np.split(data, 2, axis=1)
#print left
#for idx in range(0, amount):
#    print (left[idx] * right[idx])
#print right

num_sgmts = len(left) / sgmt
print num_sgmts
clip_num_sgmts = num_sgmts * sgmt


left_sgmts = np.array_split(left[:clip_num_sgmts], num_sgmts)
right_sgmts = np.array_split(right[:clip_num_sgmts], num_sgmts)

sgmt = len(left_sgmts[0])
print sgmt

for i in range(len(left_sgmts)):
    corr = np.correlate(left_sgmts[i][:, 0], right_sgmts[i][:, 0], mode="full")

    print corr.shape
    print "Max cor", np.amax(corr)
    print "Min cor", np.amin(corr)
    pos_sample_pos = np.argmax(corr)
    neg_sample_pos = np.argmin(corr)
    if abs(np.amax(corr)) < abs(np.amin(corr)):
        sample_pos = neg_sample_pos
        print "Negative polarity is True"
    else:
        sample_pos = pos_sample_pos
    print "Pos Sample position", pos_sample_pos
    print "Neg sample position", neg_sample_pos
    print "Variance", np.var(corr)
    print "Std Dev", np.std(corr)
    print "Significance", np.amax(corr) / np.std(corr)
    print "Confidence: {:.2%}".format(-1 / (np.amax(corr) / np.std(corr)) + 1)
    delay = sample_pos - sgmt + 1
    print delay
    delay_sec = float(delay) * 0.000022676
    #Positive value means left is ahead of right (A ahead of D)
    #Positive means remove some analog delay
    #Negative value means left is behind right (A behind D)
    #Negative means add some analog delay
    print delay, delay_sec, "sec"
    print '''A positive value means analog is ahead of digital.
That means remove some analog delay. Negative means the opposite.'''
    zscore_dist = stats.zscore(corr)
    print "Z-score for sample:", zscore_dist[sample_pos]
    #plt.plot(zscore_dist)
    #plt.show(block=True)

start = sgmt - len(corr)
end = start + len(corr)

print start, end

plt.plot(xrange(start, end), corr)
plt.ylabel('cor value')
plt.axvline(x=0, color='green')
plt.show(block=True)
