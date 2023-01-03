thrift-py:
	@for f in thrifts/protocols/*.thrift; do \
		echo $${f}; \
		thrift -out $(CURDIR) --gen py $${f}; \
	done
