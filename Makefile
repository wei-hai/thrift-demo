thrift-py:
	@for f in thrift/myapp/protocols/*.thrift; do \
		echo $${f}; \
		thrift -out $(CURDIR) --gen py $${f}; \
	done
