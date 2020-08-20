"""Machine Learning models for spark."""
from pyspark.ml import Pipeline
from pyspark.ml.evaluation import MulticlassClassificationEvaluator, \
    RegressionEvaluator
from pyspark.ml.feature import StringIndexer, SQLTransformer, VectorAssembler
from pyspark.ml.regression import LinearRegression
from pyspark.ml.classification import LogisticRegression
from pyspark.mllib.evaluation import MulticlassMetrics
from pyspark.sql.functions import countDistinct


def linear_regression(train_set, test_set, debug=False):
    """Linear Regression.

    :param train_set: train set
    :param test_set: test set
    :return: RMSE
    """
    vectorize = SQLTransformer(
        statement='SELECT *, vectorize_udf(text_embedding) '
                  'as text_embedding_vec FROM __THIS__'
    )
    string_indexer = StringIndexer(inputCol="subreddit",
                                   outputCol="subreddit_num")
    assembler = VectorAssembler(
        inputCols=["text_embedding_vec", "over_18", "num_comments",
                   "num_crossposts", "subreddit_num", "upvote_ratio"],
        outputCol="features")
    lr = LinearRegression(labelCol='score', featuresCol='features')
    pipeline = Pipeline(stages=[vectorize, string_indexer, assembler, lr])

    if debug:
        print("Train set")
        gr = train_set.groupBy("score").agg(countDistinct("_id"))
        gr.show()

        print("Test set")
        gr = test_set.groupBy("score").agg(countDistinct("_id"))
        gr.show()

    lrModel = pipeline.fit(train_set)
    predictions_test = lrModel.transform(test_set)
    predictions_train = lrModel.transform(train_set)
    evaluator = RegressionEvaluator(predictionCol="prediction",
                                    labelCol="score",
                                    metricName='rmse')
    evaluations = evaluator.evaluate(predictions_test), \
        evaluator.evaluate(predictions_train)

    return evaluations


def binary_classification(train_set, test_set, debug=False):
    """Binary Classification.

    :param train_set: train set
    :param test_set: test set
    :return: Weighted F1
    """
    vectorize = SQLTransformer(
        statement='SELECT *, vectorize_udf(text_embedding) '
                  'as text_embedding_vec, double(over_18) as over_18_int '
                  'FROM __THIS__'
    )
    string_indexer = StringIndexer(inputCol="subreddit",
                                   outputCol="subreddit_num")
    assembler = VectorAssembler(
        inputCols=["text_embedding_vec", "score", "num_comments",
                   "num_crossposts", "subreddit_num", "upvote_ratio"],
        outputCol="features")
    lr = LogisticRegression(labelCol='over_18_int',
                            featuresCol='features',
                            family="binomial")
    pipeline = Pipeline(stages=[vectorize, string_indexer, assembler, lr])

    if debug:
        print("Train set")
        gr = train_set.groupBy("over_18").agg(countDistinct("_id"))
        gr.show()

        print("Test set")
        gr = test_set.groupBy("over_18").agg(countDistinct("_id"))
        gr.show()

    lrModel = pipeline.fit(train_set)
    predictions = lrModel.transform(test_set)
    evaluator = MulticlassClassificationEvaluator(predictionCol="prediction",
                                                  labelCol="over_18_int",
                                                  metricName='f1')
    evaluations = evaluator.evaluate(predictions)

    if debug:
        predictions_rdd = predictions.select(['over_18_int', 'prediction']) \
            .rdd.map(lambda line: (line[1], line[0]))
        metrics = MulticlassMetrics(predictions_rdd)
        print(metrics.confusionMatrix().toArray())

        for i in range(predictions.select("over_18_int").distinct().count()):
            print("Class {} - f1: {}".format(i,
                                             metrics.fMeasure(label=float(i))))

    return evaluations


def multiclass_classification(train_set, test_set, debug=False):
    """Multiclass Classification.

    :param train_set: train set
    :param test_set: test set
    :return: Weighted F1
    """
    vectorize = SQLTransformer(
        statement='SELECT *, vectorize_udf(text_embedding) '
                  'as text_embedding_vec FROM __THIS__'
    )
    string_indexer = StringIndexer(inputCol="subreddit",
                                   outputCol="subreddit_num")
    assembler = VectorAssembler(
        inputCols=["text_embedding_vec", "score", "num_comments",
                   "num_crossposts", "over_18", "upvote_ratio"],
        outputCol="features")
    lr = LogisticRegression(labelCol='subreddit_num',
                            featuresCol='features')
    pipeline = Pipeline(stages=[vectorize, string_indexer, assembler, lr])

    if debug:
        print("Train set")
        gr = train_set.groupBy("subreddit").agg(countDistinct("_id"))
        gr.show()

        print("Test set")
        gr = test_set.groupBy("subreddit").agg(countDistinct("_id"))
        gr.show()

    lrModel = pipeline.fit(train_set)
    predictions = lrModel.transform(test_set)
    evaluator = MulticlassClassificationEvaluator(predictionCol="prediction",
                                                  labelCol="subreddit_num",
                                                  metricName="f1")
    evaluations = evaluator.evaluate(predictions)

    if debug:
        predictions_rdd = predictions.select(['subreddit_num', 'prediction']) \
            .rdd.map(lambda line: (line[1], line[0]))
        metrics = MulticlassMetrics(predictions_rdd)
        print(metrics.confusionMatrix().toArray())

        for i in range(predictions.select("subreddit_num").distinct().count()):
            print("Class {} - f1: {}".format(i,
                                             metrics.fMeasure(label=float(i))))

    return evaluations
