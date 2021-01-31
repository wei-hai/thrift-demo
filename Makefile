thrift-py:
	@for f in thrift/*.thrift; do \
		echo $${f}; \
		thrift -out $(CURDIR) --gen py $${f}; \
	done
